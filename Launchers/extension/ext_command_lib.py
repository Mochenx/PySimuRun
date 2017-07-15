#!/usr/bin/python
# encoding = utf-8

import re

__author__ = 'mochenx'


class ExtCommandLib(dict):
    all_ext_cmds = {}

    def __init__(self):
        pass

    @classmethod
    def register(cls, round_name, ext_cmd_name, ext_cmd_obj):
        ext_cmds = cls.all_ext_cmds.setdefault(round_name, {})
        ext_cmds[ext_cmd_name] = ext_cmd_obj

    def dyn_load_ext_cmds(self, ext_cmds):
        ext_cmds_lst = []
        all_cmds = re.split('\s+|,', ext_cmds)
        for a_cmd in all_cmds:
            if re.match('^\s*$', a_cmd): continue
            ext_cmds_lst.append(a_cmd)
    
        for cmd_name in ext_cmds_lst:
            for round_name in self.all_ext_cmds.keys():
                if cmd_name in self.all_ext_cmds[round_name].keys():
                    ext_cmd = self.all_ext_cmds[round_name][cmd_name]
                    if round_name not in self.keys():
                        self[round_name] = []
                    self[round_name].append(ext_cmd)

    def load(self, round_name, ext_cmd):
        if round_name not in self.keys():
            self[round_name] = []
        self[round_name].append(ext_cmd)

    def __str__(self):
        s_exist_exts = []
        for round_name in self.all_ext_cmds.keys():
            for cmd_name in self.all_ext_cmds[round_name].keys():
                s_exist_exts.append('%s-%s'%(round_name, cmd_name))

        s = '\n'.join(s_exist_exts)
        return s;
