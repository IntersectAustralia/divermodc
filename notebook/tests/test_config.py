from test_base import *

class ConfigTestCase(unittest.TestCase):
    
    def setUp(self):
        self.initial_state_config = config.load()
        file_exists(config.CONFIG_INI) 
        self.assertEqual(len(config.load()), 2)
    
    def tearDown(self):
        config.reload(self.initial_state_config)
        self.assertEqual(len(config.load()), 2)
    
    def test_initial_load(self):
        config_dict = config.load()
        self.assertEqual(len(config_dict), 2)
        
    def test_add_get_config_params(self):
        config.add('mykey1', 'myval1')
        self.assertTrue(config.get('mykey1'), 'myval1')
        config.add('mykey2', 'myval2')
        config.add('mykey1', 'myval3')
        config_dict = config.load()
        self.assertEqual(len(config_dict), 4)
        self.assertEqual(config.get('mykey1'), 'myval3')
        self.assertEqual(config.get('mykey2'), 'myval2')

    def test_reload_empty(self):
        config.reload({})
        self.assertEqual(len(config.load()), 0)
        
    def test_reload_many(self):
        config.reload({'one':1, 'two': '222 222', 'three ee e, ee': '"quick brown fox"'})
        self.assertEqual(config.get('one'), '1')
        self.assertEqual(config.get('two'), '222 222')
        self.assertEqual(config.get('three ee e, ee'), '"quick brown fox"')
        self.assertEqual(len(config.load()), 3)