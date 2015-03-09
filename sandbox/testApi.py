import sys
#import urllib2
import requests
import json
from collections import Counter
import time

f = open('event_keys.txt', 'r')
w = open('output.txt', 'w')
event_keys = f.readlines()

root = None
first = False
codes = Counter()

for event_key in event_keys:
	event_key = event_key.strip()
	r = requests.get("https://api.fda.gov/device/event.json?api_key=K81daldhUBV23QZmJMuVQBjwuNYm92Fmi9dDLjEv&search=event_key:" + event_key)

	if(r.status_code != 200):
		print r.status_code

	codes[r.status_code] += 1

	if(first == False):
		first = True
		j = json.loads(r.content)
		root = j["results"]
		continue

	j = json.loads(r.content)
	root.append(j["results"][0])
	print event_key

	time.sleep(0.5)

json.dump(root, w, indent=4)

print "Completed with the following response codes: "
for k, v in codes.items():
	print "\t" + str(k) + " : " + str(v)

f.close()
w.close()
