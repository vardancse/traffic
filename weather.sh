#!/bin/bash
start=2014-01-01
end=2014-02-01
while [ "$start" != $end ]; do
  custom_start=`echo $start | sed "s/-//g"`
  wget --output-document=New_York_City_$custom_start.json http://api.wunderground.com/api/fe5c0eae76462c31/history_$custom_start/q/NY/New_York_City.json
  start=$(date -I -d "$start + 1 day")

done
