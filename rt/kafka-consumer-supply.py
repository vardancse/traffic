from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys, traceback

es = Elasticsearch(["http://0.0.0.0:9200"], maxsize=25,timeout=100)
#kafka = KafkaClient()
KAFKA_TOPIC = "rt-supply"
ES_INDEX = "rt-feed"
ES_TYPE = "nyc-supply"
bulk_counter = 10
actions = []

consumer = KafkaConsumer(KAFKA_TOPIC,
                         group_id='my-group',
                         bootstrap_servers=['localhost:9092'])

for message in consumer:
	bulk_counter = bulk_counter-1
        #print message
	#print type(message)
	#print message.value
	try:
                action = {
                "_op_type":"index",
                "_index": ES_INDEX,
                "_type": ES_TYPE,
                "_source":message.value
                }
                actions.append(action)
		if(bulk_counter==0):
                	helpers.bulk(es,actions)
			print 'Batch has been indexed'
			bulk_counter=10
			actions=[]
        except Exception:
                traceback.print_exc()
print len(actions)
helpers.bulk(es,actions)
