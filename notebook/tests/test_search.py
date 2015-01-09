from test_base import *
# pip install sure, pip install httpretty
from sure import expect
import httpretty

class SearchTestCase(unittest.TestCase):
    
    def setUp(self):
        self.token = '12345'
        self.myhost = 'http://somehost'
        self.myurl = '%s/%s' % (self.myhost, hiev.SEARCH_URL_FRAGMENT)
        self.initial_config_state = config.load()
        hiev.set_token(self.token)
        hiev.set_host(self.myhost)
    
    def tearDown(self):
        config.reload(self.initial_config_state)

    # define callback function
    def request_callback(self, request, uri, headers):
        print uri
        self.assertEquals(uri, self.expected_uri)
        import json
        j = json.dumps([{'file_id':137, 'filename':'returned.txt'}])
        return (200, headers, j) 
        
    @httpretty.activate
    def test_search_filename(self):              
        myfile = 'myfile.egg'
        url_params = 'auth_token=%s&filename=%s' % (self.token, myfile)
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        
        results = hiev.search(filename=myfile, quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])

    @httpretty.activate
    def test_search_description(self):              
        desc = 'some crazy description @#SJDOFJ!! se../`~, ^$%(+ END.'
        url_params = 'auth_token=%s&description=%s' % (self.token, 'some+crazy+description+%40%23SJDOFJ%21%21+se..%2F%60~%2C+%5E%24%25%28%2B+END.')
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        
        results = hiev.search(description=desc, quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])        
     
    @httpretty.activate
    def test_search_all_non_list_args(self):              
        myfile = 'myfile.egg'
        from_date = 'x'
        to_date = 'y'
        description = 'desc'
        file_id='137'
        id='337'
        uploader_id='999'
        url_params = 'description=desc&uploader_id=999&auth_token=12345&filename=myfile.egg&from_date=x&file_id=137&id=337&to_date=y'
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        
        results = hiev.search(filename=myfile, 
                              from_date=from_date, 
                              to_date=to_date, 
                              description=description, 
                              file_id=file_id,
                              id=id,
                              uploader_id = uploader_id,
                              quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])        
        
    
    def test_search_file_formats(self):
        return
    
    def test_search_variables(self):
        return
    
    def test_search_all_list_args(self):
        return
    
     
        