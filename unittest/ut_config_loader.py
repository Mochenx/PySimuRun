#!/usr/bin/python
# encoding = utf-8


import unittest
from Launchers.config_loader import ConfigBuiltinExt, UnsetRoundException
from Launchers.config_loader import ConfigExtension
from Launchers.config_loader import ConfigLoader


class UTBuiltinExt(unittest.TestCase):
    def test_new_ext_no_round(self):
        m = ConfigBuiltinExt({'name': 'a_module'})
        self.assertEqual(m.name, 'a_module')
        self.assertRaises(UnsetRoundException, lambda: m.compile_round)
        self.assertRaises(UnsetRoundException, lambda: m.run_round)

    def test_new_ext_round(self):
        m = ConfigBuiltinExt({'name': 'b_module',
                              'round': {'compile': '1', 'run': '2'}})
        self.assertEqual(m.name, 'b_module')
        self.assertEqual(m.compile_round, '1')
        self.assertEqual(m.run_round, '2')


class UTConfigExtension(unittest.TestCase):
    def test_new_ext_no_spaces(self):
        s_expt = 'Launchers.extension.a_module'
        m = ConfigExtension('a_module')
        self.assertEqual(m.ext_path, s_expt)

    def test_new_ext_spaces(self):
        s_expt = 'Launchers.extension.a_module'
        m = ConfigExtension('   a_module  ')
        self.assertEqual(m.ext_path, s_expt)


class UTConfigLoader(unittest.TestCase):
    def test_load_cfg_yaml(self):
        ext_names = ['ext1', 'ext2']
        cfg_ldr = ConfigLoader('test_config_ld.yaml')

        m_cases = cfg_ldr.get('cases')
        self.assertEqual(m_cases.compile_round, 1)
        self.assertEqual(m_cases.run_round, 2)

        m_gui = cfg_ldr.get('gui')
        self.assertRaises(UnsetRoundException, lambda: m_gui.compile_round)
        self.assertRaises(UnsetRoundException, lambda: m_gui.run_round)

        m_dump = cfg_ldr.get('dumpoff')
        self.assertRaises(UnsetRoundException, lambda: m_dump.compile_round)
        self.assertRaises(UnsetRoundException, lambda: m_dump.run_round)

        for i, ext in enumerate(cfg_ldr):
            self.assertEqual(ext.ext_name, ext_names[i])

    def test_dyn_import_ext(self):
        ConfigBuiltinExt.to_ext_path = 'extension4test'
        ConfigExtension.to_ext_path = 'extension4test'
        cfg_ldr = ConfigLoader('test_config_ld.yaml')
        m_cases = cfg_ldr.get('cases')
        dyn_module = m_cases.load()
        self.assertEqual(dyn_module.cases.cmp_case.compile_round, 1)
        self.assertEqual(dyn_module.cases.cmp_case.run_round, 2)

        for i, ext in enumerate(cfg_ldr):
            if ext.ext_name == 'ext1':
                dyn_module = ext.load()
                self.assertEqual(dyn_module.ext1.local_var, 112358)
