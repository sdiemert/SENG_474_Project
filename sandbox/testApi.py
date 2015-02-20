import sys
#import urllib2
import requests
import json


r = requests.get("https://api.fda.gov/device/event.json?limit=25")

j = json.loads(r.content)
print json.dumps(j)
