import json
import os
from elasticsearch import Elasticsearch
from elasticsearch import helpers
es = Elasticsearch(["http://localhost:9200"], maxsize=25,timeout=100)
ES_INDEX = 'weather'
ES_TYPE = 'nyc'
actions=[]
static_path='/data/traffic/weather/'
for file in os.listdir("/data/codebase/weather"):
	json_data=open(static_path+file).read()
	data = json.loads(json_data)
	print 'going for ',file	
	for hour in data['history']['observations']:
		row={}
		weather_time=hour['date']['year']+'-'+hour['date']['mon']+'-'+hour['date']['mday']+' '+hour['date']['hour']+':'+hour['date']['min']+':00'
		row['weather_time']=weather_time.replace(' ','T')+'Z'
		row['tempm']=hour['tempm']
		row['snow']=hour['snow']
		row['hum']=hour['hum']
		row['rain']=hour['rain']
		row['conds']=hour['conds']
		row['tornado']=hour['tornado']
		row['fog']=hour['fog']
		try:
	                action = {
	                "_op_type":"index",
	                "_index": ES_INDEX,
	                "_type": ES_TYPE,
	                "_source":row
	                }
	                actions.append(action)
        	except Exception:
                	traceback.print_exc()
helpers.bulk(es,actions)
