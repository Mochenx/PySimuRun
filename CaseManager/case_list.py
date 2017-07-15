#!/usr/bin/python
# encoding = utf-8

import os
import re
import sys
from os import path


__author__ = 'mochenx'


if sys.version_info[0] == 3:
    py3k = True
else:
    py3k = False
if py3k:
    from functools import reduce
    func_reduce = reduce
    func_input = input
else:
    func_reduce = reduce
    func_input = raw_input


class TestBenchEnv(object):
    case_dir = '../../cases'


# Test case discovery
class TestCaseRecognizer(object):
    @staticmethod
    def is_a_test_case(tc_path):
        return True


class Case(object):
    """
    (case path, case name)
    """
    def __init__(self, case_pattern, case_path, case_name):
        self._case = (case_path, case_name)
        self.pattern = case_pattern

    @property
    def case(self):
        return self._case

    @property
    def name(self):
        return self._case[1]

    @property
    def path(self):
        return self._case[0]

    def __str__(self):
        return ('%s' % os.path.sep).join([self.case[0], self.case[1]])


class CaseList(list):
    """
    It supposes that a test case here is a group of files or data resided in a directory, so this class
        provides a list of the paths of cases which are matched with given pattern

    Pseudo-code
    if the case pattern is a path(either an absolute path or relative path):
        Scan the path
        if exists an argument of choosing a case:
            Return the selected case
        else:
            Return all cases in returned case list
    else:
        Scan predefined root case directory
        if len of case list is one:
            Return it
        else if the pattern matches only the path part of all cases:
            Return all cases in returned case list
        else if exists an argument of running all cases:
            Return all cases in returned case list
        else:
            Return the selected case
    """
    case_recognizer = TestCaseRecognizer
    cases_for_compile = None

    def __init__(self, scan_path, case_pattern):
        self.scan_path = scan_path
        self.case_pattern = case_pattern

    def _get_case_list(self):
        self.scan_dir_for_case()
        self.filter_case_list()

    def filter_case_list(self):
        raise NotImplementedError()

    @classmethod
    def get_case_list(cls, tc_pattern):
        new_tc = None
        if path.isdir(tc_pattern):
            all_matched_tc = CasesListFromPath(scan_path=tc_pattern, case_pattern=tc_pattern)
        else:
            all_matched_tc = CasesListFromRegEx(scan_path=TestBenchEnv.case_dir, case_pattern=tc_pattern)
        all_matched_tc._get_case_list()
        if len(all_matched_tc) > 0:
            new_tc = all_matched_tc
        return new_tc

    def scan_dir_for_case(self):
        for work_dir, sub_dirs, _ in os.walk(self.scan_path):
            if len(sub_dirs) > 0:
                # Don't walk into SVN/Git subdirectory
                for i, _dir in enumerate(sub_dirs[:]):
                    if re.match(r'^(\.svn|\.git)$', _dir):
                        del sub_dirs[i]
            if re.match(r'.*%s.*' % self.case_pattern, work_dir) and self.case_recognizer.is_a_test_case(work_dir):
                work_dir = work_dir.rstrip(os.path.sep)
                new_case = Case(case_pattern=self.case_pattern,
                                case_path=os.path.dirname(work_dir),
                                case_name=os.path.basename(work_dir))
                self.append(new_case)  # Yes, it is a test case


class CasesListFromPath(CaseList):
    """
    if exists an argument of choosing a case:
        Return the selected case
    else:
        Return all cases in returned case list
    """
    def filter_case_list(self):
        return


class CasesListFromRegEx(CaseList):
    """
    if len of case list is one:
        Return it
    else if the pattern matches only the path part of all cases:
        Return all cases in returned case list
    else if exists an argument of running all cases:
        Return all cases in returned case list
    else:
        Return the selected case
    """
    def filter_case_list(self):
        func_check_each_path = lambda x, y: self.check_each_path(x, y)

        if len(self) == 1:
            return
        elif func_reduce(func_check_each_path, self, True):
            return
        else:
            self.select_n_filter()

    def check_each_path(self, accumulated_items, item):
        only_match_path = False
        if not isinstance(item, Case):
            raise TypeError('One given cases of is not type of Case')
        if re.match(r'.*%s.*' % self.case_pattern, item.case[0]):
            only_match_path = True
        return accumulated_items and only_match_path

    def select_n_filter(self):
        for i, case in enumerate(self):
            print('%0d) %s' % (i, str(case)))
        input_again = True
        while input_again:
            user_sel = func_input('Please input the number:')
            if not re.match(r'\d+', user_sel):
                print("%s isn't a valid digit" % user_sel)
            elif int(user_sel) >= len(self):
                print('Please input a number from 0 to %0d' % (len(self) - 1))
            else:
                input_again = False

        case_selection = int(user_sel)
        sel_case = self[case_selection]
        if py3k:
            self.clear()
        else:
            del self[:]
        self.append(sel_case)


