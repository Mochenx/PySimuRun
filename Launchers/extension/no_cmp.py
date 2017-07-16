#!/usr/bin/python
# encoding = utf-8

from ext_command_lib import ExtCommandLib

from Launchers.extension.ext_cmp_opts import ExtCmpOpts

__author__ = 'mochenx'

__all__ = ['no_cmp']


class NoCmp(ExtCmpOpts):
    def __init__(self):
        ExtCommandLib.register('workflow', 'no_cmp', self)

    def __call__(*args, **kwargs):
        if args[0] != 'run':
            return False
        return True

no_cmp = NoCmp()
