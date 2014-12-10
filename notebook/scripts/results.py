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
print 'Results:'

# pretty print result
print json.dumps(results, sort_keys=True, indent=2, separators=(',',': '))


