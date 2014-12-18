# pip install requests
import requests
import json

# Generate token in DIVER

token = raw_input('Copy and paste your DIVER token here: ')
payload = {'stati':'RAW','auth_token':token}
respd = requests.post('http://localhost:3000/data_files/api_search', params=payload)
results = json.loads(respd.text)

# print report
print ''
print 'Search results: %s' % len(results)
print 'Files returned:'

# pretty print result
#print json.dumps(results, sort_keys=True, indent=2, separators=(',',': '))
for f in results:
    print "Filename: %s  (ID: %s)" % (f['filename'], f['file_id'])

# download first resulted file
file1 = results[0]
filename = file1['filename']
url = "http://localhost:3000/data_files/%s/download" % file1['file_id']
payload = {'auth_token':token}
r = requests.get(url, params=payload, stream = True)
print r
with open(filename, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
            f.flush()

