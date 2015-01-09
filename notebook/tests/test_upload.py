from test_base import *
from sure import expect
import httpretty

class UploadTestCase(unittest.TestCase):
    
    def setUp(self):
        self.token = '12345'
        self.myhost = 'http://somehost'
        self.myurl = '%s/%s' % (self.myhost, hiev.UPLOAD_FILE_URL_FRAGMENT)
        self.initial_config_state = config.load()
        hiev.set_token(self.token)
        hiev.set_host(self.myhost)
    
    def tearDown(self):
        config.reload(self.initial_config_state)

    # define callback function
    def request_callback(self, request, uri, headers):
        print uri
        self.assertEquals(uri, self.expected_uri)  
        print request.body     
        return (200, headers, 'Success\n') 
        
    @httpretty.activate
    def test_upload(self):
        file_to_upload = '%s/tests/data/testfile.txt' % PROJECT_ROOT
        exp_id = 21
        type = 'RAW'
        url_params = 'auth_token=12345&type=RAW&experiment_id=21'
        self.expected_uri = '%s%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        hiev.upload(file_to_upload, exp_id, type)
        