import json
from collections import Counter
import time

output = open('output.txt', 'r')
w = open('parsedOutput.arff', 'w')

parsedOutput = json.loads(output.read())

manufacturers = []
operators = []
occupation_codes = []
product_codes = []



for record in parsedOutput:
	device_operator = record["device"][0]['device_operator'].replace(" ", '-').replace(",", "") if "device" in record.keys() and "device_operator" in record["device"][0].keys() else '?'
	
	if(device_operator not in operators):
		operators.append(device_operator)

	manufacturer_name = record["manufacturer_name"].replace(" ", '-').replace(",", "") if "manufacturer_name" in record.keys() else '?'

	if(manufacturer_name not in manufacturers):
		manufacturers.append(manufacturer_name)

	reporter_occupation_code = record["reporter_occupation_code"].replace(" ", '-').replace(",", "") if "reporter_occupation_code" in record.keys() else '?'

	if(reporter_occupation_code not in occupation_codes):
		occupation_codes.append(reporter_occupation_code)	

	device_report_product_code = record["device"][0]["device_report_product_code"].replace(" ", '-').replace(",", "") if "device" in record.keys() and "device_report_product_code" in record["device"][0].keys() and record["device"][0]["device_report_product_code"] != '' else '?'

	if(device_report_product_code not in product_codes):
		product_codes.append(device_report_product_code)

w.write('@RELATION\tliability\n')
w.write('@ATTRIBUTE\tmanufacturer_name\t{' + ','.join(["'" + m + "'" for m in manufacturers]) + '}\n')
w.write('@ATTRIBUTE\tdevice_operator\t{' + ','.join(["'" + o + "'" for o in operators]) + '}\n')
w.write('@ATTRIBUTE\treporter_occupation_code\t{' + ','.join(["'" + oc + "'" for oc in occupation_codes]) + '}\n')
w.write('@ATTRIBUTE\tdevice_report_product_code\t{' + ','.join(["'" + pc + "'" for pc in product_codes]) + '}\n')
w.write('@ATTRIBUTE\texpired\t{TRUE,FALSE}\n')
w.write("@ATTRIBUTE\tclass\t{'Death','Injury','Malfunction','Other','No answer provided'}\n\n")
w.write('@DATA\n')

for record in parsedOutput:
	manufacturer_name = record["manufacturer_name"] if "manufacturer_name" in record.keys() else '?'
	event_type = record["event_type"] if record["event_type"] else '?'
	device_operator = record["device"][0]['device_operator'] if "device" in record.keys() and "device_operator" in record["device"][0].keys() else '?'
	reporter_occupation_code = record["reporter_occupation_code"] if "reporter_occupation_code" in record.keys() else '?'
	device_report_product_code = record["device"][0]["device_report_product_code"] if "device" in record.keys() and "device_report_product_code" in record["device"][0].keys() and record["device"][0]["device_report_product_code"] != '' else '?'
	
	date_of_event = record["date_of_event"] if "date_of_event" in record.keys() else None
	expiration_date_of_device = record["device"][0]["expiration_date_of_device"] if "device" in record.keys() and "expiration_date_of_device" in record["device"][0].keys() else None

	expired = 'FALSE'

	if(date_of_event != None and expiration_date_of_device != None):
		parsedDateOfEvent = time.strptime(date_of_event, "%Y%m%d")
		parsedExpiration = time.strptime(expiration_date_of_device, "%Y%m%d")

		if(parsedDateOfEvent != None and parsedExpiration != None):
			expired = 'TRUE' if parsedDateOfEvent >= parsedExpiration else 'FALSE'
	

	w.write("'" + manufacturer_name.replace(" ", '-').replace(",", "") + "'" + ',' + "'" + device_operator.replace(" ", '-').replace(",", "") + "'" + ',' + "'" + reporter_occupation_code.replace(" ", '-').replace(",", "") + "'" + ',' + "'" + device_report_product_code.replace(" ", '-').replace(",", "") + "'" + ',' + str(expired) + "," + "'" + event_type + "'" + '\n')

output.close()
w.close()