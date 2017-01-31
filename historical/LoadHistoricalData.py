import os
import csv
import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import Geohash
import traceback
import datetime

csvfilename = '/data/dataset/green_tripdata_2014-01.csv'
#jsonfilename = csvfilename.split('.')[0] + '.json'
csvfile = open(csvfilename, 'r')
#jsonfile = open(jsonfilename, 'w')
reader = csv.DictReader(csvfile)
timeDateSuffix = '_datetime'
fieldnames = ('VendorID','lpep_pickup_datetime','Lpep_dropoff_datetime','Store_and_fwd_flag','RateCodeID','Pickup_longitude','Pickup_latitude','Dropoff_longitude','Dropoff_latitude','Passenger_count','Trip_distance','Fare_amount','Extra','MTA_tax','Tip_amount','Tolls_amount','Ehail_fee','Total_amount','Payment_type')

es = Elasticsearch(["http://localhost:9200"], maxsize=25,timeout=100)
ES_INDEX = 'traffic_may_2016'
ES_TYPE = 'green'
output = []
actions =[]
i=0
for each in reader:
	print i
	i=i+1
        row = {}
        for field in fieldnames:
                if field.endswith(timeDateSuffix):
                    each[field] = each[field].replace(' ','T')+'Z'
                row[field] = each[field]
        row['pickup_geohash'] = Geohash.encode(float(each['Pickup_latitude']),float(each['Pickup_longitude']),7)
	row['dropoff_geohash'] = Geohash.encode(float(each['Dropoff_latitude']),float(each['Dropoff_longitude']),7)
	row['elapsed_time'] = (datetime.datetime.strptime(each['Lpep_dropoff_datetime'], '%Y-%m-%dT%H:%M:%SZ')-datetime.datetime.strptime(each['lpep_pickup_datetime'], '%Y-%m-%dT%H:%M:%SZ')).seconds
	if row['elapsed_time'] >0:
		row['speed'] = round(float(each['Trip_distance'])*60*60/float(row['elapsed_time']))
	'''try:
		row['surge_indicator_fare'] = round(float(float(each['fare_amount'])/float(each['trip_distance'])),2)
	except Exception:
		row['surge_indicator_fare']=0
	'''
	#print row
	#r=json.dumps(row)
	#print r
	try:
        	action = {
       		"_op_type":"index",
        	"_index": ES_INDEX,
        	"_type": ES_TYPE,
		"_source":row
        	}
        	actions.append(action)	
		#helpers.bulk(es,actions)
	except Exception:
        	traceback.print_exc()
helpers.bulk(es,actions)

