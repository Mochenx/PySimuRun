#!/usr/bin/python
# encoding = utf-8

from ext_command_lib import ExtCommandLib

from Launchers.extension.ext_sim_opts import ExtSimOpts

__author__ = 'mochenx'

__all__ = ['uvm_low', 'uvm_medium', 'uvm_high', 'uvm_debug']


class UVMLow(ExtSimOpts):
    def __init__(self):
        ExtCommandLib.register('run', 'uvm_low', self)

    def __call__(self, *args, **kwargs):
        return '+UVM_VERBOSITY=UVM_LOW'

class UVMMedium(ExtSimOpts):
    def __init__(self):
        ExtCommandLib.register('run', 'uvm_medium', self)

    def __call__(self, *args, **kwargs):
        return '+UVM_VERBOSITY=UVM_MEDIUM'

class UVMHigh(ExtSimOpts):
    def __init__(self):
        ExtCommandLib.register('run', 'uvm_high', self)

    def __call__(self, *args, **kwargs):
        return '+UVM_VERBOSITY=UVM_HIGH'


class UVMDebug(ExtSimOpts):
    def __init__(self):
        ExtCommandLib.register('run', 'uvm_debug', self)

    def __call__(self, *args, **kwargs):
        return '+UVM_VERBOSITY=UVM_DEBUG'

uvm_low = UVMLow()
uvm_medium = UVMMedium()
uvm_high = UVMHigh()
uvm_debug = UVMDebug()
