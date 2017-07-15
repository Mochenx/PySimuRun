#!/usr/bin/python
# encoding = utf-8

from Launchers.config_loader import ConfigLoader


__all__ = ['cmp_case']


class Cases:
    def __init__(self):
        ext = ConfigLoader.get('cases')
        self.compile_round = ext.compile_round
        self.run_round = ext.run_round
        print('Load extension: "cases" successfully')

cmp_case = Cases()
