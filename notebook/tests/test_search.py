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
        
    @httpretty.activate  
    def test_search_file_formats(self):
        file_formats = ['f1', 'f2', 'f3']
        url_params = 'file_formats%5B%5D=f1&file_formats%5B%5D=f2&file_formats%5B%5D=f3&auth_token=12345'
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        results = hiev.search(file_formats=file_formats, quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])        
    
    @httpretty.activate
    def test_search_variables(self):
        variables = ['sdflkj', 'wrijdf', 'selfj']
        url_params = 'variables%5B%5D=sdflkj&variables%5B%5D=wrijdf&variables%5B%5D=selfj&auth_token=12345'
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        results = hiev.search(variables=variables, quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])     
    
    @httpretty.activate
    def test_search_all_list_args(self):
        file_formats = ['f1', 'f2', 'f3']
        stati = ['RAW', 'PROCESSED']
        published=['true']
        unpublished=['true','false']
        experiments=['3', '5', '64']
        variables = ['sdflkj', 'wrijdf', 'selfj']
        url_params = 'variables%5B%5D=sdflkj&variables%5B%5D=wrijdf&variables%5B%5D=selfj&stati%5B%5D=RAW&stati%5B%5D=PROCESSED&file_formats%5B%5D=f1&file_formats%5B%5D=f2&file_formats%5B%5D=f3&auth_token=12345&published%5B%5D=true&experiments%5B%5D=3&experiments%5B%5D=5&experiments%5B%5D=64&unpublished%5B%5D=true&unpublished%5B%5D=false'
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        results = hiev.search(file_formats=file_formats, 
                              variables=variables, 
                              stati=stati,
                              unpublished=unpublished,
                              experiments=experiments,
                              published=published,
                              quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])     
        
    
    @httpretty.activate
    def test_search_all_args(self):
        myfile = 'myfile.egg'
        from_date = 'x'
        to_date = 'y'
        description = 'desc'
        file_id='137'
        id='337'
        uploader_id='999'
        tags= ['t1', 't2']
        facilities=['aaa','bbb','ccc']
        file_formats = ['f1', 'f2', 'f3']
        stati = ['RAW', 'PROCESSED']
        published=['true']
        unpublished=['true','false']
        published_date='z'
        experiments=['3', '5', '64']
        variables = ['sdflkj', 'wrijdf', 'selfj']
        url_params = 'variables%5B%5D=sdflkj&variables%5B%5D=wrijdf&variables%5B%5D=selfj&published%5B%5D=true&stati%5B%5D=RAW&stati%5B%5D=PROCESSED&description=desc&uploader_id=999&experiments%5B%5D=3&experiments%5B%5D=5&experiments%5B%5D=64&auth_token=12345&tags%5B%5D=t1&tags%5B%5D=t2&facilities%5B%5D=aaa&facilities%5B%5D=bbb&facilities%5B%5D=ccc&from_date=x&to_date=y&published_date=z&unpublished%5B%5D=true&unpublished%5B%5D=false&file_formats%5B%5D=f1&file_formats%5B%5D=f2&file_formats%5B%5D=f3&filename=myfile.egg&id=337&file_id=137'
        self.expected_uri = '%s?%s' % (self.myurl, url_params)
        httpretty.register_uri(httpretty.POST, self.myurl, body=self.request_callback)
        results = hiev.search(filename=myfile,
                              file_formats=file_formats, 
                              from_date=from_date,
                              to_date=to_date,
                              description=description,
                              file_id=file_id,
                              id=id,
                              stati=stati,
                              published=published,
                              unpublished=unpublished,
                              published_date=published_date,
                              tags=tags,
                              facilities=facilities,
                              experiments=experiments,
                              variables=variables, 
                              uploader_id=uploader_id,
                              quiet=True)
        self.assertEquals(1, len(results))
        self.assertEquals(137, results[0]['file_id'])   
     
        