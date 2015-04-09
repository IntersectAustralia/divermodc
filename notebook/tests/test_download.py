from test_base import *
from sure import expect
import httpretty

class DownloadTestCase(unittest.TestCase):
    
    def setUp(self):
        self.token = '12345'
        self.myhost = 'http://somehost'
        self.initial_config_state = config.load()
        hiev.set_token(self.token)
        hiev.set_host(self.myhost)
    
    def tearDown(self):
        config.reload(self.initial_config_state)

    # define callback function
    def request_callback(self, request, uri, headers):
        #print(uri)
        self.assertEqual(uri, self.expected_uri)       
        return (200, headers, 'Success\n') 
        
    @httpretty.activate
    def test_download(self):
        import json
        fileid = 137
        filename = 'returned.txt'
        j = json.dumps([{'file_id': fileid, 'filename': filename}])
        metadata = json.loads(j)
        download_fragment = hiev.DOWNLOAD_FILE_URL_FRAGMENT % fileid
        url = '%s/%s' % (self.myhost, download_fragment) 
        self.expected_uri = '%s?auth_token=12345' % url
        httpretty.register_uri(httpretty.GET, url, body=self.request_callback)
        dest = '/tmp'
        hiev.download(metadata, dest)
        f = '%s/%s' % (dest, filename)
        file_exists(f)
        os.remove(f)
        
        