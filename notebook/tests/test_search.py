from test_base import *
import requests
# pip install sure, pip install httpretty
from sure import expect
import httpretty

class SearchTestCase(unittest.TestCase):
    
    def setUp(self):
        return
    
    def tearDown(self):
        return


    
    @httpretty.activate
    def test_search(self):       
        
        def request_callback(request, uri, headers):
            return (200, headers, "The {} response from {}".format(request.method, uri))

        
        hiev.set_token('12345')
        myhost = "http://somehost"
        hiev.set_host(myhost)
        myurl ='%s/%s?filename=myfile.egg&auth_token=12345&quiet=False' % (myhost, hiev.SEARCH_URL_FRAGMENT)
        print myurl
        httpretty.register_uri(httpretty.POST, myurl, body=request_callback)
        hiev.search(filename="myfile.egg")
        