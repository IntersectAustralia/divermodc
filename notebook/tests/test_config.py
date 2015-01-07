from test_base import *

class ConfigTestCase(unittest.TestCase):
    
    def setUp(self):
        self.initial_state_config = config.load()
        import os.path
        file_exists = os.path.exists(config.CONFIG_INI) 
        assert file_exists
        self.assertEquals(len(config.load()), 2)
    
    def tearDown(self):
        config.reload(self.initial_state_config)
        self.assertEquals(len(config.load()), 2)
    
    def test_initial_load(self):
        config_dict = config.load()
        self.assertEquals(len(config_dict), 2)
        
    def test_add_get_config_params(self):
        config.add('mykey1', 'myval1')
        self.assertTrue(config.get('mykey1'), 'myval1')
        config.add('mykey2', 'myval2')
        config.add('mykey1', 'myval3')
        config_dict = config.load()
        self.assertEquals(len(config_dict), 4)
        self.assertEquals(config.get('mykey1'), 'myval3')
        self.assertEquals(config.get('mykey2'), 'myval2')

    def test_reload_empty(self):
        config.reload({})
        self.assertEquals(len(config.load()), 0)
        
    def test_reload_many(self):
        config.reload({'one':1, 'two': '222 222', 'three ee e, ee': '"quick brown fox"'})
        self.assertEquals(config.get('one'), '1')
        self.assertEquals(config.get('two'), '222 222')
        self.assertEquals(config.get('three ee e, ee'), '"quick brown fox"')
        self.assertEquals(len(config.load()), 3)