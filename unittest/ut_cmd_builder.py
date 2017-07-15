#!/usr/bin/python
# encoding = utf-8


import unittest
from Launchers.simu_cmd_builder import SimuCmdBuilder


class UTCmdBuilder(unittest.TestCase):
    def test_plus_catenate_fail(self):
        ret = SimuCmdBuilder.plus_catenate([1, 2, 3])
        self.assertIsNone(ret)

    def test_plus_catenate_ok_1(self):
        s_ret = SimuCmdBuilder.plus_catenate({'+define': ['AA']})
        print(s_ret)
        self.assertEqual(s_ret, '+define+AA')

    def test_plus_catenate_ok_12(self):
        s_ret = SimuCmdBuilder.plus_catenate({'+define': ['AA', 'BB']})
        print(s_ret)
        self.assertEqual(s_ret, '+define+AA+BB')

    def test_plus_catenate_ok_22(self):
        s_expt = ['+define+AA+BB', '+incdir+CC+DD']
        s_ret = SimuCmdBuilder.plus_catenate({'+define': ['AA', 'BB'], '+incdir': ['CC', 'DD']})
        print(s_ret)
        s_ret_lst = s_ret.split(' ')
        for i, s in enumerate(sorted(s_ret_lst)):
            self.assertEqual(s, s_expt[i])

    def test_traverse_simple(self):
        expt_lst = ['cmd', '-1', '-2', '-3']
        cmd_lst = SimuCmdBuilder.traverse(expt_lst)
        self.assertEqual(cmd_lst, expt_lst)

    def test_traverse_nest_list(self):
        expt_lst = ['cmd', '-1', '-2', '-3', '-4']
        cmd_lst = SimuCmdBuilder.traverse(['cmd', '-1', '-2', ['-3', '-4']])
        self.assertEqual(cmd_lst, expt_lst)

    def test_traverse_nest_dict(self):
        expt_lst = ['cmd', '-1', '-2', '+define+AA+BB']
        cmd_lst = SimuCmdBuilder.traverse(['cmd', '-1', '-2', {'+define': ['AA', 'BB']}])
        self.assertEqual(cmd_lst, expt_lst)

    def test_parse_yaml(self):
        expt_lst = ['cmd', 'opt1', 'opt2', '+D+m1+m2 +I+i1+i2']
        parsed_yaml = SimuCmdBuilder('test_cmd_builder.yaml')
        self.assertEqual(parsed_yaml.rounds, ['round1'])
        cmd_seqs = parsed_yaml.get_command_seq('round1')
        self.assertEqual(len(expt_lst), len(cmd_seqs))
        last_item = cmd_seqs[-1].split(' ')
        cmd_seqs[-1] = ' '.join(sorted(last_item))
        self.assertEqual(cmd_seqs, expt_lst)
