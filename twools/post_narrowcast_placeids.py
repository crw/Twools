import os
import json
import pprint

import requests
from requests_oauthlib import OAuth1Session
import yaml


pp = pprint.PrettyPrinter(indent=4)

test_place_ids = [
    '6416b8512febefc9',
    '30410557050f13a5',
    '78bfaf3f12c05982',
    '8d65596349ee2e01',
    'c29833e68a86e703',
    'e7c97cdfef3a741a',
    'f3bfc7dcc928977f',
    'fdcd221ac44fa326',
    '2ee7eeaa84dbe65a',
    'ea679934779f45c7',
    'c799e2d3a79f810e',
    '06ef846bfc783874',
    '879d7cfc66c9c290',
    '0ce8b9a7b2742f7e',
    '5714382051c06d1e',
    'ecdce75d48b13b64',
    '82b141af443cb1b8',
    '4e7c21fd2af027c6',
    '682c5a667856ef42',
    '8198e85105936d3c',
    'a9928b6eaeb54f86',
    '1ef1183ed7056dc1',
    '6b5d375c346e3be9',
    '58f54743b1a62911',
    'c3932d3da7922986',
    '34ed2e67dd5a22bb',
    'd5cde4dddd7e6f94',
    '81b8dcbe189773f2',
    'f0af1239cbebb474',
    'f7531639e8db5e12',
    '7dc97830ee71b3cb',
    '084d0d0155787e9d',
    '1d834adff5d584df',
    '9778812ea3fffe48',
    'd0e642e8a900f679',
    'e222580e9a58b499',
    '82779978c58253a6',
    'c9506eee1d5f5143',
    '60fcb78e1f3a23dd',
    'a89b926651acf416',
    '333a5811d6b0c1cb',
    '0a51cbf77aee0006',
    '6c990e36e6fa8033',
    'db367491e0c03477',
    'd9a15239f67eec6d',
    '96683cc9126741d1']

post_status_url = 'https://api.twitter.com/1.1/statuses/update.json'
status = """
Country: {}
PlaceID: {}"""

f = open(os.path.expanduser('~/.twurlrc'), 'r')
twurlrc = yaml.load(f.read())

default_profile = twurlrc['configuration']['default_profile'][0]
default_consumer = twurlrc['configuration']['default_profile'][1]

user_token = twurlrc['profiles'][default_profile][default_consumer]['token']
user_secret = twurlrc['profiles'][default_profile][default_consumer]['secret']
app_key = twurlrc['profiles'][default_profile][default_consumer]['consumer_key']
app_secret = twurlrc['profiles'][default_profile][default_consumer]['consumer_secret']

twitter = OAuth1Session(app_key,
			            client_secret=app_secret,
			            resource_owner_key=user_token,
			            resource_owner_secret=user_secret)

if os.path.isfile('pid_cache.json'):
    with open('pid_cache.json', 'r') as f:
        pid_map = json.loads(f.read())
else:
    pid_map = {}
    response = twitter.get('https://ads-api.twitter.com/0/targeting_criteria/locations?location_type=COUNTRY')
    place_ids = json.loads(response.content)
    for pid in place_ids['data']:
        pid_map[pid['targeting_value']] = pid['name']
    with open('pid_cache.json', 'w') as f:
        f.write(json.dumps(pid_map))

print "Posting start"
r = twitter.post(post_status_url,
                data={ 'status': 'Opening test post' })

for pid in test_place_ids:
    st = status.format(pid_map[pid], pid)
    print "Posting {}".format(st)
    r = twitter.post(post_status_url,
                    data={ 'status': st, 'narrowcast_place_ids': pid })
    if r.status_code is not requests.codes.ok:
        print "Bad Status Code discovered:"
        print r.status_code
        print r.text
        print ""


print "Posting end"
r = twitter.post(post_status_url,
                data={ 'status': 'Ending test post' })
