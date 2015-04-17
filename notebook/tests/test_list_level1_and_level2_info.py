from test_base import *
# pip install sure, pip install httpretty
from sure import expect
import httpretty


class ListLevel1AndLevel2InfoTestCase(unittest.TestCase):
    def setUp(self):
        self.token = '12345'
        self.myhost = 'http://somehost'
        self.myurl = '%s/%s' % (self.myhost, hiev.LEVEL1_AND_LEVEL2_INFO_URL_FRAGMENT)
        self.initial_config_state = config.load()
        hiev.set_token(self.token)
        hiev.set_host(self.myhost)

    def tearDown(self):
        config.reload(self.initial_config_state)

    # define callback function
    def request_callback(self, request, uri, headers):
        #print(uri)
        #self.assertEqual(uri, self.expected_uri)
        import json

        j = json.dumps([
            {'facility_id': 1,
             'facility_name': "xxx",
             'experiments': [{'id': 23, 'name': "Rain Experiment"}, {'id': 49, 'name': "blah"}]},
            {'facility_id': 2,
             'facility_name': "YYY",
             'experiments': [{'id': 12, 'name': "Some Experiment"}]},
            {'facility_id': 3,
             'facility_name': "Zzz",
             'experiments': []}
        ])
        return 200, headers, j

    @httpretty.activate
    def test_list_level1_and_level2_info(self):
        url_params = 'auth_token=%s' % (self.token)
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.GET, self.myurl, body=self.request_callback)

        results = hiev.list_level1_and_level2_info(quiet=True)
        self.assertEqual(3, len(results))
        self.assertEqual(2, len(results[0]['experiments']))
        self.assertEqual(1, len(results[1]['experiments']))
        self.assertEqual(0, len(results[2]['experiments']))
        self.assertEqual(1, results[0]['facility_id'])
        self.assertEqual(2, results[1]['facility_id'])
        self.assertEqual(3, results[2]['facility_id'])
        self.assertEqual("xxx", results[0]['facility_name'])
        self.assertEqual("YYY", results[1]['facility_name'])
        self.assertEqual("Zzz", results[2]['facility_name'])
        self.assertEqual(23, results[0]['experiments'][0]['id'])
        self.assertEqual(49, results[0]['experiments'][1]['id'])
        self.assertEqual(12, results[1]['experiments'][0]['id'])
        self.assertEqual('Rain Experiment', results[0]['experiments'][0]['name'])
        self.assertEqual('blah', results[0]['experiments'][1]['name'])
        self.assertEqual('Some Experiment', results[1]['experiments'][0]['name'])
