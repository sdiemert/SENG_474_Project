import sys
#import urllib2
import requests
import json
from collections import Counter
import time

skip = 0
i = 0
first = False

r = requests.get("https://api.fda.gov/device/event.json?search=date_received:[20140101+TO+20150101]&skip=0")

while r.status_code != 404:
	w = open('./raw_data/output' + str(skip) + '-' + str(skip + 10000) + '.txt', 'w')
	results = []

	while i < skip + 10000:
		r = requests.get("https://api.fda.gov/device/event.json?search=date_received:[19910101+TO+20150101]&limit=100&skip=" + str(i))

		j = json.loads(r.content)
		for result in j["results"]:
			results.append(result)

		time.sleep(0.5)

		i += 100

		print "Completed records " + str(i - 100)  + " to " + str(i)		

	skip += 10000
	json.dump(results, w, indent=4)	
	w.close()