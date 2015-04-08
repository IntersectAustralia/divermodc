"""
API to the search functionality of DIVER
Required library: pip install requests
"""

from urllib.parse import urljoin
import requests
import json
from diver.logger import log
import diver.config as config
import sys

# Ignore SSL warnings for now
import warnings
warnings.filterwarnings('ignore')

SEARCH_URL_FRAGMENT = "data_files/api_search"
DOWNLOAD_FILE_URL_FRAGMENT = "data_files/%s/download"
UPLOAD_FILE_URL_FRAGMENT = "data_files/api_create?"
VARLIST_URL_FRAGMENT = "data_files/variable_list"

VAR_NAME = "name"
VAR_UNIT = "unit"
VAR_DATA_TYPE = "data_type"
VAR_FILL_VALUE = "fill_value"
VAR_COLUMN_MAPPING = "mapping"
VARLIST = [VAR_NAME, VAR_UNIT, VAR_DATA_TYPE, VAR_FILL_VALUE, VAR_COLUMN_MAPPING]

class InvalidTokenError(Exception): {}
class EmptyTokenError(Exception): {}
class EmptyHostError(Exception): {}

def set_token(token):
    config.add("token",token)

def set_host(diver_host):
    config.add("host_url",diver_host)
    
def set_downloaded_files_dir(dest):
    config.add("downloaded_files_dir", dest)    

def search(filename=None,
              file_formats=None,
              from_date=None,
              to_date=None,
              #exclude=None,
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
    payload = check_params(payload)
    log(payload)
    
    try:
        diver_host = config.get("host_url")
        diver_token = config.get("token")
        if not diver_host:
            raise EmptyHostError
        if not diver_token:
            raise EmptyTokenError
        url = urljoin(diver_host, SEARCH_URL_FRAGMENT)
        if (not quiet):
            print ("Posting Query to " + url)
        respd = requests.post(url, params = payload, verify=False)
        results = json.loads(respd.text)
        if isinstance(results, dict) and results.has_key("error"):
            raise KeyError
            
        # pretty print result to log file
        log(pretty_print_json(results))
        
        if (not quiet):
            print ('Search results: ' + str(len(results)))
            print ('Files returned:')
            for f in results:
                print ("Filename: " + f['filename'] + "ID: " + str(f['file_id']))
        return results
    
    except requests.ConnectionError:
        print ('[Error] Cannot connect the url ' + diver_host + '. Please check your url, run "set_host(url)" and try again.')
    except KeyError:
        print ('[Error] Invalid Key: ' + diver_token + ' Please check your token, run "set_token(token)" and try again.')
    except EmptyHostError:
        print ("[Error] Please set DIVER host url by set_host('..') or edit config.ini file.")
    except EmptyTokenError:
        print ("[Error] Please set DIVER token by set_token('..') or edit config.ini file.")
    except Exception as e:
        print (e)
        
def is_url_valid(url):
    import urlparse
    parsed_url = urlparse.urlparse(url)
    return bool(parsed_url.scheme)  
      
def payload_builder(param_dict={}):
    token = config.get("token")
    param_dict['auth_token'] = token
    return param_dict
    
def check_params(param_dict):         
    for key, value in param_dict.items() :
        if isinstance(value, list) and not key[-2:] == '[]': 
            param_dict[key + '[]'] = value
            param_dict.pop(key)
    # remove 'quiet=False'
    param_dict.pop('quiet')        
    return param_dict    
    
def download(files_metadata, dest=None):
    try:
        diver_host = config.get("host_url")
        diver_token = config.get("token")
        if not diver_host:
            raise EmptyHostError
        if not diver_token:
            raise EmptyTokenError    
        if not dest:
            dest = config.get("downloaded_files_dir")
        url = urljoin(diver_host, DOWNLOAD_FILE_URL_FRAGMENT)
        for f in files_metadata:
            filename = f['filename']
            fid = f['file_id']
            download_url = url % fid
            d_resp = requests.get(download_url, params=payload_builder(), stream=True, verify=False)
            save_file_downloaded(filename, d_resp, dest)
    except requests.ConnectionError:
        print ('[Error] Cannot connect the url ' + diver_host + '. Please check your url, run "set_host(url)" and try again.')
    except KeyError:
        print ('[Error] Invalid Key: ' + diver_token + '. Please check your token, run "set_token(token)" and try again.')
    except EmptyHostError:
        print ("[Error] Please set DIVER host url by set_host('..') or edit config.ini file.")
    except EmptyTokenError:
        print ("[Error] Please set DIVER token by set_token('..') or edit config.ini file.") 
    except Exception as e:
        print (e)

def upload(filepath, experiment_id, type):
    try:
        diver_host = config.get("host_url")
        diver_token = config.get("token")
        if not diver_host:
            raise EmptyHostError
        if not diver_token:
            raise EmptyTokenError    
        url = urljoin(diver_host, UPLOAD_FILE_URL_FRAGMENT)
        print ('Uploading file ' + filepath + 'to ' + url)
        filename = get_filename(filepath)
        file =  open(filepath, 'rb')
        files = {'file': (filename, file, type, {'Expires': '0'})}
        payload = payload_builder({'experiment_id':experiment_id, 'type':type})
        log(payload)
        u_resp = requests.post(url, params=payload, files=files, verify=False)
        log(u_resp)
        if not u_resp:
            print ('[Error] Upload arguments invalid or incomplete.')
        else:
            print ('Upload Complete!')
        return u_resp
    except requests.ConnectionError:
        print ('[Error] Cannot connect the url ' + diver_host + '. Please check your url, run "set_host(url)" and try again.')
    except KeyError:
        print ('[Error] Invalid Key: ' + diver_token + '. Please check your token, run "set_token(token)" and try again.')
    except EmptyHostError:
        print ("[Error] Please set DIVER host url by set_host('..') or edit config.ini file.")
    except EmptyTokenError:
        print ("[Error] Please set DIVER token by set_token('..') or edit config.ini file.") 
    except Exception as e:
        print (e)

def get_variables(var_list_json, key, quiet=False):
    if key not in VARLIST:
        print ('No such variable: ' + key)
        print ('Try one of these:') 
        print (VARLIST)
        return
    var_set = set()
    for var in var_list_json:
        if key in var and var[key]:
          var_set.add(var[key])
    # print if not quiet
    if not quiet:
        print ('\nAll "' + key + '" variables:\n')
        for var in var_set:
            print (var)
    return var_set

def list_variables(quiet=False):
    try:
        diver_host = config.get("host_url")
        diver_token = config.get("token")
        if not diver_host:
            raise EmptyHostError
        if not diver_token:
            raise EmptyTokenError    
        url = urljoin(diver_host, VARLIST_URL_FRAGMENT)
        print ('Retrieving all variables from ' + url)
        payload = payload_builder()
        
        u_resp = requests.post(url, params=payload)
        results = json.loads(u_resp.text)
        if isinstance(results, dict) and results.has_key("error"):
            raise KeyError
        # pretty print result to log file
        log(pretty_print_json(results))
        
        if (not quiet):
            print ('Search results: ' + str(len(results)))
            print ('Variables returned:')
            for var in results:
                print ("Name: %s" % var[VAR_NAME])
                if VAR_UNIT in var:
                    print ("Unit: %s" % var[VAR_UNIT])
                if VAR_DATA_TYPE in var:
                    print ("Data Type: %s" % var[VAR_DATA_TYPE])
                if VAR_FILL_VALUE in var:
                    print ("Fill Value: %s" % var[VAR_FILL_VALUE])
                if VAR_COLUMN_MAPPING in var:
                    print ("Column Mapping: %s" % var[VAR_COLUMN_MAPPING])
                print ("")
        return results
    except requests.ConnectionError:
        print ('[Error] Cannot connect the url ' + diver_host + '. Please check your url, run "set_host(url)" and try again.')
    except KeyError:
        print ('[Error] Invalid Key: ' + diver_token + '. Please check your token, run "set_token(token)" and try again')
    except EmptyHostError:
        print ("[Error] Please set DIVER host url by set_host('..') or edit config.ini file.")
    except EmptyTokenError:
        print ("[Error] Please set DIVER token by set_token('..') or edit config.ini file.")
    except Exception as e:
        print (e)
        
def get_filename(filepath):
    import ntpath
    return ntpath.basename(filepath)

def save_file_downloaded(filename, respond, dest):
    print ("Downloading " + filename)
    import os.path
    filepath = os.path.join(dest, filename)
    with open(filepath, "wb") as f:
        for chunk in respond.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()
    print ("Saved as " + filepath)
    log("Downloaded %s as %s" % (filename, filepath))

def pretty_print_json(str):
    return json.dumps(str, sort_keys=True, indent=2, separators=(',',': '))
    
