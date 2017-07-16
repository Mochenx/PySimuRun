#!/usr/bin/python
# encoding = utf-8


import unittest
import re
from Launchers.simu_workflow import SimuWorkflow
from Launchers.extension import *
from CaseManager.case_list import Case


class ExtPreStart(ExtCmpOpts):
    def __init__(self):
        ExtCommandLib.register('pre_start', 'go', self)

    def __call__(self, *args, **kwargs):
        cmd_seq = args[0][-1]
        assert(cmd_seq == 'wrong_pre_start')
        args[0].pop(-1)
        return ['pre_start']


class ExtPostStart(ExtCmpOpts):
    def __init__(self):
        ExtCommandLib.register('post_start', 'go', self)

    def __call__(self, *args, **kwargs):
        cmd_seq = args[0][-1]
        assert(cmd_seq == 'wrong_post_start')
        args[0].pop(-1)
        return ['post_start']


class ExtRun(ExtSimOpts):
    def __init__(self):
        ExtCommandLib.register('run', 'go', self)

    def __call__(self, *args, **kwargs):
        return kwargs['tc_name']


class UTWorkflow(unittest.TestCase):
    def test_start(self):
        expt_cmp_log = ['----- Running: echo pre_start',
                        '----- Running: echo start working',
                        '----- Running: echo post_start']
        # Clean the contents of 'cmp.log'
        f = open('cmp.log', 'w')
        f.close()

        # Go through work flow
        ut_launcher = SimuWorkflow()
        ut_launcher.start('ut_workflow.yaml', {'pre_start': [ExtPreStart()],
                                               'post_start': [ExtPostStart()]})
        # Check the results
        with open('cmp.log', 'r') as f:
            s_all = f.read()
        valid_log_cnt = 0
        for ln in s_all.split('\n'):
            if re.match(r'^\s*$', ln) is None:
                self.assertEqual(ln.lstrip(' ').rstrip(' '), expt_cmp_log[valid_log_cnt])
                valid_log_cnt += 1

    def test_run(self):
        expt_sim_log = 'pre_run\nA\nstart running\n_no_case\nB\npost_run\n'
        # Clean the contents of 'cmp.log'
        f = open('sim.log', 'w')
        f.close()
        # Go through simulation
        SimuWorkflow.do_case_link = False
        f_get_seed = lambda: 12
        ut_launcher = SimuWorkflow()
        ut_launcher.run_cases('ut_sim_template.yaml', [Case('no_case', '../case', 'no_case')],
                              f_get_seed, 1, {'run': [ExtRun()]})
        with open('sim.log', 'r') as f:
            s_all = f.read()
        self.assertEqual(s_all, expt_sim_log)
