#!/usr/bin/python
# encoding = utf-8

import Launchers.yaml as yaml
import os

__author__ = 'mochenx'


class UnsetRoundException(Exception):
    pass


class ConfigBuiltinExt:
    """
    In calling function, e.g. the main function of run, the followings will execute
        cases = ConfigBuiltinExt(...)
        cases.load calls __import__ to import the corresponding extension (Python module).
    Then
        The extension will get its target rounds by calling ConfigLoader.get, and register itself to that round
    """
    to_ext_path = 'Launchers.extension'

    def __init__(self, cfg_dict):
        assert('name' in cfg_dict)
        self._name = cfg_dict['name']
        if 'round' in cfg_dict and 'compile' in cfg_dict['round']:
            self._compile_round_name = cfg_dict['round']['compile']
        else:
            self._compile_round_name = None
        if 'round' in cfg_dict and 'run' in cfg_dict['round']:
            self._run_round_name = cfg_dict['round']['run']
        else:
            self._run_round_name = None

    @property
    def name(self):
        return self._name

    @property
    def compile_round(self):
        if self._compile_round_name is None:
            raise UnsetRoundException
        return self._compile_round_name

    @property
    def run_round(self):
        if self._run_round_name is None:
            raise UnsetRoundException
        return self._run_round_name

    def load(self):
        ext_name = self.name.lstrip(' ').rstrip(' ')
        return __import__(self.to_ext_path + '.' + ext_name)


class ConfigExtension:
    to_ext_path = 'Launchers.extension'

    def __init__(self, ext_name):
        self.ext_name = ext_name.lstrip(' ').rstrip(' ')
        self.ext_path = self.to_ext_path + '.' + self.ext_name
        print('Load extension module: %s' % self.ext_path)

    def load(self):
        return __import__(self.ext_path)


class ConfigLoader(list):
    """
    Format of .config.yaml:
        cases:
            name: cases
            round:
                compile: TB_n_case
                run: run

        gui:
            name: gui

        dump:
            name: dump

        extension_list:
            - uvm_verbosity
            - no_cmp

    Each builtin extension, e.g. cases, calls ConfigLoader.get('cases') to get known to which round it registers
    """
    ext_list_key_name = 'extension_list'
    _builtin_ext = {'cases': None, 'gui': None, 'dump': None}

    def __init__(self, cfg_path):
        self.all_cfg = None
        self.parse_cfg(cfg_path)

    def parse_cfg(self, cfg_path):
        f = open(cfg_path, 'r')
        s_all = f.read()
        f.close()
        self.all_cfg = yaml.load(s_all)
        assert(isinstance(self.all_cfg, dict))
        for k in self._builtin_ext.keys():
            if k in self.all_cfg:
                self._builtin_ext[k] = ConfigBuiltinExt(self.all_cfg[k])
        if self.ext_list_key_name in self.all_cfg:
            self.load_ext_module()

    def load_ext_module(self):
        ext_list = self.all_cfg[self.ext_list_key_name]
        assert(isinstance(ext_list, list))
        for ext_name in ext_list:
            assert(isinstance(ext_name, str))
            new_ext_module = ConfigExtension(ext_name)
            self.append(new_ext_module)

    @classmethod
    def get(cls, builtin_ext_name):
        """
        :param builtin_ext_name:
            The name(string) of builtin extension
        :return:
            An object of ConfigBuiltinExt
        """
        if builtin_ext_name in cls._builtin_ext:
            return cls._builtin_ext[builtin_ext_name]
