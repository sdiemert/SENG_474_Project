import json
from collections import Counter
import time

output = open('raw_data/merged.txt', 'r')
w = open('parsedOutput.arff', 'w')

parsedOutput = json.loads(output.read().decode("utf-8-sig"))

manufacturers = []
operators = []
occupation_codes = []
product_codes = []

for record in parsedOutput:

	try:
		if type(record["device"]) is not list or len(record["device"]) <= 0:
			continue

		device_operator = record["device"][0]['device_operator'].replace("'", '').replace(",", "") if "device" in record.keys() and "device_operator" in record["device"][0].keys() else '?'
		
		if(device_operator.encode('ascii') not in operators and device_operator.encode('ascii') != ''):
			operators.append(device_operator.encode('ascii'))

		manufacturer_name = record["manufacturer_name"].replace("'", '').replace(",", "") if "manufacturer_name" in record.keys() else '?'

		if(manufacturer_name.encode('ascii') not in manufacturers and manufacturer_name.encode('ascii') != ''):
			manufacturers.append(manufacturer_name.encode('ascii'))

		reporter_occupation_code = record["reporter_occupation_code"].replace("'", '').replace(",", "") if "reporter_occupation_code" in record.keys() else '?'

		if(reporter_occupation_code.encode('ascii') not in occupation_codes and reporter_occupation_code.encode('ascii') != ''):
			occupation_codes.append(reporter_occupation_code.encode('ascii'))	

		device_report_product_code = record["device"][0]["device_report_product_code"].replace("'", '').replace(",", "") if "device" in record.keys() and "device_report_product_code" in record["device"][0].keys() and record["device"][0]["device_report_product_code"] != '' else '?'

		if(device_report_product_code.encode('ascii') not in product_codes and device_report_product_code.encode('ascii') != ''):
			product_codes.append(device_report_product_code.encode('ascii'))
	except UnicodeEncodeError:
		continue

manufacturers.append('')
operators.append('')
occupation_codes.append('')
product_codes.append('')

w.write('@RELATION\tliability\n')
w.write('@ATTRIBUTE\tmanufacturer_name\t{' + ','.join(["'" + m + "'" for m in manufacturers]) + '}\n')
w.write('@ATTRIBUTE\tdevice_operator\t{' + ','.join(["'" + o + "'" for o in operators]) + '}\n')
w.write('@ATTRIBUTE\treporter_occupation_code\t{' + ','.join(["'" + oc + "'" for oc in occupation_codes]) + '}\n')
w.write('@ATTRIBUTE\tdevice_report_product_code\t{' + ','.join(["'" + pc + "'" for pc in product_codes]) + '}\n')
w.write('@ATTRIBUTE\texpired\t{TRUE,FALSE}\n')
w.write("@ATTRIBUTE\tclass\t{'Death','Injury','Malfunction','Other','No answer provided','?'}\n\n")
w.write('@DATA\n')

for record in parsedOutput:
	try:
		if type(record["device"]) is not list or len(record["device"]) <= 0:
			continue

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
		

		w.write("'" + manufacturer_name.replace("'", '').replace(",", "").encode('ascii') + "'" + ',' + "'" + device_operator.replace("'", '').replace(",", "").encode('ascii') + "'" + ',' + "'" + reporter_occupation_code.replace("'", '').replace(",", "").encode('ascii') + "'" + ',' + "'" + device_report_product_code.replace("'", '').replace(",", "").encode('ascii') + "'" + ',' + str(expired).encode('ascii') + "," + "'" + event_type.encode('ascii') + "'" + '\n')
	except UnicodeEncodeError:
		continue
output.close()
w.close()