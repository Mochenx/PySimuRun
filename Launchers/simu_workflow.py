#!/usr/bin/python
# encoding = utf-8


import subprocess
from os.path import exists
import os
from simu_cmd_builder import SimuCmdBuilder
from CaseManager.case_list import TestBenchEnv


__author__ = 'mochenx'


class RunCmdException(Exception):
    pass


class SimuWorkflow(object):
    cmp_log_tmp_name = '.cmp-pysimurun-tmp.log'
    cmp_log_name = 'cmp.log'
    seed_file_name = 'rnd_seed'
    call_cmd_env = os.environ;

    def __init__(self, dump_off=False):
        self.cmp_log_file = None
        self.dump_off = dump_off

    def call_cmd_n_append_log(self, cmd):
        if not exists(self.cmp_log_name):
            self.cmp_log_file = open(self.cmp_log_name, 'w')
        else:
            self.cmp_log_file = open(self.cmp_log_name, 'a')
        print('\n----- Running: %s \n\n' % ' '.join(cmd))
        self.cmp_log_file.writelines('\n----- Running: %s \n\n' % ' '.join(cmd))
        retcode = subprocess.call(cmd, env=self.call_cmd_env)

        try:
            cmp_tmp_log_file = open(self.cmp_log_tmp_name, 'r')
            self.cmp_log_file.write(cmp_tmp_log_file.read())
            cmp_tmp_log_file.close()
        except IOError:
            pass
        if retcode is None or retcode > 0:
            self.cmp_log_file.close()
            raise RunCmdException()

        self.cmp_log_file.close()

    def start(self, run_cfg_path, ext_cmds_lib):
        cmd_seqs = SimuCmdBuilder(run_cfg_path)
        for round_name in cmd_seqs:
            exe_cmd_seq = True
            cmd_seq = cmd_seqs.get_command_seq(round_name)
            if round_name in ext_cmds_lib.keys():
                for cmd in ext_cmds_lib[round_name]:
                    cmd_seq.extend(cmd(cmd_seq))
            if 'workflow' in ext_cmds_lib:
                for flow_ctrl in ext_cmds_lib['workflow']:
                    if not flow_ctrl(round_name, cmd_seq):
                        exe_cmd_seq = False
            if exe_cmd_seq:
                self.call_cmd_n_append_log(cmd_seq)
        
    def run_cases(self, sim_cfg_path, test_cases, f_get_seed, repeat_times, ext_cmds_lib):
        for one_tc in test_cases:
            tc_name = '_' + one_tc.name
            for _ in range(repeat_times):
                pre_cmds, run_cmd, post_cmds = self.get_run_cmds(sim_cfg_path)
                print(run_cmd)
                seed = f_get_seed()
                if 'run' in ext_cmds_lib.keys():
                    for cmd in ext_cmds_lib['run']:
                        run_cmd.append(cmd(tc_name=tc_name, seed=seed))
                print(' '.join(run_cmd))
                # Execute Pre-run commands
                os.system('rm -f %s' % TestBenchEnv.running_tc_link)
                os.system('ln -s %s %s' % (str(one_tc), TestBenchEnv.running_tc_link))
                for cmd_seq in pre_cmds:
                    os.system(' '.join(cmd_seq))
                # Issue run simulation command
                os.system(' '.join(run_cmd))
                # Execute Post-run commands
                for cmd_seq in post_cmds:
                    os.system(' '.join(cmd_seq))

                # Collect simulation results to a folder
                if len(test_cases) > 1 or repeat_times > 1:
                    self.collect_simu_rslts(one_tc, seed)

    def get_run_cmds(self, sim_cfg_path):
        run_cmds_seq = SimuCmdBuilder(sim_cfg_path)
        i, pre_post_cmds = 0, [[], []]
        run_cmd = None
        for round_name in run_cmds_seq:
            if round_name == 'run':
                run_cmd = run_cmds_seq.get_command_seq('run')
                i += 1
                continue
            else:
                pre_post_cmds[i].append(run_cmds_seq.get_command_seq(round_name))
        return pre_post_cmds[0], run_cmd, pre_post_cmds[1]

    def collect_simu_rslts(self, one_tc, seed):
        if not exists(TestBenchEnv.regression_path):
            os.system('mkdir %s' % TestBenchEnv.regression_path)
        rgr_path_list = ['%s', '%s_%0d' % (TestBenchEnv.regression_path, one_tc.name, seed)]
        case_log_folder_name = os.path.sep.join(rgr_path_list) + os.path.sep
        if not exists(case_log_folder_name):
            os.system('mkdir %s' % case_log_folder_name)
        for rslt_pattern in TestBenchEnv.collect_result_list:
            os.system('mv -f %s %s' % (rslt_pattern, case_log_folder_name))
        os.system('mv -f %s %s' % (self.seed_file_name, case_log_folder_name))

