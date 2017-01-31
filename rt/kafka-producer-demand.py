from kafka import KafkaProducer
import json
import random
import datetime
import time
import Geohash

KAFKA_TOPIC = "rt-demand"
KAFKA_HOST = "localhost:9092"
file='lat-long.txt'
 
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
print "start producing to: " + KAFKA_TOPIC


def randomDemand():
	lines = open(file).read().splitlines()
	latlong = random.choice(lines)
	lat = latlong.split(',')[0]
	long = latlong.split(',')[01]
	userID = random.randrange(0, 10000)
	requestTime = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
	row ={}
 	row['latitude'] = lat
 	row['longtitude'] = long
 	row['userID'] = userID
 	row['requestTime'] = requestTime
	row['geohash'] = Geohash.encode(float(lat),float(long),7)
 	return row

try:
	while(True): 
		producer.send(KAFKA_TOPIC,randomDemand())
		producer.flush()
		time.sleep(2)
except Exception as ex:
	print ex
