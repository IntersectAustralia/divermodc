"""
API to the search functionality of DIVER

Required library: pip install requests
"""

from urlparse import urljoin
import requests
import json
from logger import log

HOST = "http://localhost:3000"
SEARCH_URL_FRAGMENT = "data_files/api_search"
DOWNLOAD_FILE_URL_FRAGMENT = "data_files/%s/download"
DOWNLOAD_DEST = "/Users/veronica/Downloads/files"
TOKEN_FILE = "token.txt"

def set_token(token):
    tokfile = open(TOKEN_FILE, "w+")
    tokfile.write(token)
    tokfile.flush()
    tokfile.close()
    
def search(filename=None,
              file_formats=None,
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
    # print payload
    url = urljoin(HOST, SEARCH_URL_FRAGMENT)
    respd = requests.post(url, params = payload)
    results = json.loads(respd.text)
    
    # pretty print result to log file
    log(json.dumps(results, sort_keys=True, indent=2, separators=(',',': ')))

    print 'Search results: %s' % len(results)
    print 'Files returned:'
    for f in results:
        print "Filename: %s  (ID: %s)" % (f['filename'], f['file_id'])
    return results

def payload_builder(param_dict={}):
    try:
        tokfile = open(TOKEN_FILE, "r")
        token = tokfile.readline()
        tokfile.close()    
        param_dict['auth_token'] = token
    except IOError:
        print "Please set token first!"
        return None
    return param_dict
    
    
def download(files):
    url = urljoin(HOST, DOWNLOAD_FILE_URL_FRAGMENT)
    for f in files:
        filename = f['filename']
        fid = f['file_id']
        download_url = url % fid
        d_resp = requests.get(download_url, params=payload_builder(), stream=True)
        save_file_downloaded(filename, d_resp, DOWNLOAD_DEST)
    return

def save_file_downloaded(filename, respond, dest):
    print "Downloading %s" % filename 
    import os.path
    filepath = os.path.join(dest, filename)
    with open(filepath, "wb") as f:
        for chunk in respond.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print "Saved as %s" % filepath
    log("Downloaded %s as %s" % (filename, filepath))

        