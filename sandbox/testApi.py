import sys
#import urllib2
import requests
import json

f = open('event_keys.txt', 'r')
w = open('output.txt', 'w')
event_keys = f.readlines()

root = None
first = False

for event_key in event_keys:
	event_key = event_key.strip()
	r = requests.get("https://api.fda.gov/device/event.json?search=event_key:" + event_key)

	if(first == False):
		first = True
		j = json.loads(r.content)
		root = j["results"]
		continue

	root.append(j["results"][0])
	print event_key

json.dump(root, w, indent=4)

f.close()
w.close()
