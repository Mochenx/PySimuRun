#!/usr/bin/python
# encoding = utf-8

import Launchers.yaml as yaml

__author__ = 'mochenx'


class SimuCmdBuilder(list):
    def __init__(self, run_cfg_path):
        f = open(run_cfg_path, 'r')
        s_all = f.read()
        f.close()
        self._all_cmds = {}
        for round_desc in yaml.load(s_all):
            round_name = round_desc['name']
            self.append(round_name)
            self._all_cmds[round_name] = self.traverse(round_desc['command'])

    def get_command_seq(self, round_name):
        return self._all_cmds[round_name]

    @property
    def rounds(self):
        return list(self._all_cmds.keys())

    @staticmethod
    def traverse(cmd_seq):
        """ Do a traverse of parsed YAML structure, and form a command sequence """

        cmd_list = []
        for cmd_elem in cmd_seq:
            if isinstance(cmd_elem, list):
                # A sub-command sequence
                cmd_list.extend(SimuCmdBuilder.traverse(cmd_elem))
            elif isinstance(cmd_elem, dict):
                # A argument sequence catenated by '+'  
                plus_cat_cmd_elem = SimuCmdBuilder.plus_catenate(cmd_elem)
                if plus_cat_cmd_elem is not None:
                    cmd_list.append(plus_cat_cmd_elem)
            else:
                # Common argument
                    cmd_list.append(cmd_elem)
        return cmd_list

    @staticmethod
    def plus_catenate(dict_to_be_cat):
        if not isinstance(dict_to_be_cat, dict):
            return None

        ret_cmds = []
        for key in dict_to_be_cat.keys():
            cmds = []
            cmds.append(key)
            cmds.extend(dict_to_be_cat[key])
            ret_cmds.append('+'.join(cmds))
        return ' '.join(ret_cmds)


if __name__ == '__main__':
    cmd_seqs = SimuCmdBuilder('run_cfg.yaml')
    for round_name in cmd_seqs:
        print(cmd_seqs.get_command_seq(round_name))
