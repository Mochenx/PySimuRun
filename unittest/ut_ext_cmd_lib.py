#!/usr/bin/python
# encoding = utf-8


import unittest
from Launchers.extension import *


class ExtForTest(ExtCmpOpts):
    def __init__(self, label4test, round_id, ext_id):
        ExtCommandLib.register('round%d' % round_id, 'ext%d' % ext_id, self)
        self.label4test = label4test

    def __call__(self, *args, **kwargs):
        return self.label4test

ext1 = ExtForTest(11235, 1, 1)
ext2 = ExtForTest(235811, 1, 2)
ext12 = ExtForTest(31415, 2, 12)


class ExtSimForTest(ExtSimOpts):
    def __init__(self, label4simu):
        ExtCommandLib.register('run', 'simu_ext1', self)
        self.label4simu = label4simu

    def __call__(self, *args, **kwargs):
        return self.label4simu


simu_ext = ExtSimForTest(15926)


class ManualExtForTest(ExtCmpOpts):
    def __call__(self, *args, **kwargs):
        return 'manual'


ext_m = ManualExtForTest()


class UTExtCmdLib(unittest.TestCase):
    def test_register_ext1_space(self):
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext_not_exist')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertNotIn('ext_not_exist', ext_lib['round1'])
        for ext_cmd in ext_lib['round1']:
            self.assertEqual(ext_cmd(), 11235)

    def test_register_ext1_comma(self):
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1, ext_not_exist')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertNotIn('ext_not_exist', ext_lib['round1'])
        for ext_cmd in ext_lib['round1']:
            self.assertEqual(ext_cmd(), 11235)

    def test_register_ext1_ext2(self):
        expt_rslts = [11235, 235811]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext2')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(ext2, ext_lib['round1'])
        for i, ext_cmd in enumerate(ext_lib['round1']):
            self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_register_rounds(self):
        expt_rslts = [11235, 31415]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext12')
        self.assertIn('round1', ext_lib)
        self.assertIn('round2', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(ext12, ext_lib['round2'])
        # 'round1' is before 'round2' in order
        for i, k in enumerate(sorted(ext_lib.keys())):
            for ext_cmd in ext_lib[k]:
                self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_register_cmp_sim(self):
        expt_rslts = [11235, 15926]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 simu_ext1')
        self.assertIn('round1', ext_lib)
        self.assertIn('run', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(simu_ext, ext_lib['run'])
        # 'round1' is before 'run' in order
        for i, k in enumerate(sorted(ext_lib.keys())):
            for ext_cmd in ext_lib[k]:
                self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_manually_register(self):
        ext_lib = ExtCommandLib()
        ext_lib.load('round_m', ext_m)
        self.assertIn('round_m', ext_lib)
        self.assertIn(ext_m, ext_lib['round_m'])
        # 'round1' is before 'run' in order
        for ext_cmd in ext_lib['round_m']:
            return 'manual'


ext_m = ManualExtForTest()


class UTExtCmdLib(unittest.TestCase):
    def test_register_ext1_space(self):
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext_not_exist')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertNotIn('ext_not_exist', ext_lib['round1'])
        for ext_cmd in ext_lib['round1']:
            self.assertEqual(ext_cmd(), 11235)

    def test_register_ext1_comma(self):
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1, ext_not_exist')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertNotIn('ext_not_exist', ext_lib['round1'])
        for ext_cmd in ext_lib['round1']:
            self.assertEqual(ext_cmd(), 11235)

    def test_register_ext1_ext2(self):
        expt_rslts = [11235, 235811]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext2')
        self.assertIn('round1', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(ext2, ext_lib['round1'])
        for i, ext_cmd in enumerate(ext_lib['round1']):
            self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_register_rounds(self):
        expt_rslts = [11235, 31415]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 ext12')
        self.assertIn('round1', ext_lib)
        self.assertIn('round2', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(ext12, ext_lib['round2'])
        # 'round1' is before 'round2' in order
        for i, k in enumerate(sorted(ext_lib.keys())):
            for ext_cmd in ext_lib[k]:
                self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_register_cmp_sim(self):
        expt_rslts = [11235, 15926]
        ext_lib = ExtCommandLib()
        ext_lib.dyn_load_ext_cmds('ext1 simu_ext1')
        self.assertIn('round1', ext_lib)
        self.assertIn('run', ext_lib)
        self.assertIn(ext1, ext_lib['round1'])
        self.assertIn(simu_ext, ext_lib['run'])
        # 'round1' is before 'run' in order
        for i, k in enumerate(sorted(ext_lib.keys())):
            for ext_cmd in ext_lib[k]:
                self.assertEqual(ext_cmd(), expt_rslts[i])

    def test_manually_register(self):
        ext_lib = ExtCommandLib()
        ext_lib.load('round_m', ext_m)
        self.assertIn('round_m', ext_lib)
        self.assertIn(ext_m, ext_lib['round_m'])
        # 'round1' is before 'run' in order
        for ext_cmd in ext_lib['round_m']:
            self.assertEqual(ext_cmd(), 'manual')
