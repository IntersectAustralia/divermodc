"""
API to the search functionality of DIVER
"""

from urlparse import urljoin
import requests
import json

HOST = "http://localhost:3000"
SEARCH_URL_FRAGMENT = "data_files/api_search"
FILE_URL_FRAGMENT = "data_files/%s/download"
DOWNLOAD_DEST = "/User/veronica/Downloads"
TOKEN_FILE = "token.txt"

def set_token(token):
    tokfile = open(TOKEN_FILE, "w+")
    tokfile.write(token)
    tokfile.flush()
    tokfile.close()
    
def search(filename=None,
              from_date=None,
              to_date=None,
              exclude=None,
              description=None,
              file_id=None,
              id=None,
              stati=None,
              published=None,
              unpublished=None,
              published_date=None,
              tags=None,
              facilities=None,
              experiments=None,
              variables=None,
              uploader_id=None,
              #showFiles=10,
              #fileVersion=None,
              quiet=False
              ):
    param_dict = locals()
    payload = payload_builder(param_dict);
    print payload
    url = urljoin(HOST, SEARCH_URL_FRAGMENT)
    respd = requests.post(url, params = payload)
    results = json.loads(respd.text)
    # pretty print result
    print json.dumps(results, sort_keys=True, indent=2, separators=(',',': '))
    return results

def payload_builder(param_dict):
    tokfile = open(TOKEN_FILE, "r")
    token = tokfile.readline()
    tokfile.close()    
    param_dict['auth_token'] = token
    return param_dict
    
    
def download(files):
    return
    

    
        
        