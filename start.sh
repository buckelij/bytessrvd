#!/bin/bash
#create user
cd /opt/bytessrvd/elasticsearch
/opt/bytessrvd/elasticsearch/bin/elasticsearch > /opt/bytessrvd/elasticsearch.log  2>&1 &
sleep 10
cd /opt/bytessrvd/logstash
/opt/bytessrvd/logstash/bin/logstash -f /opt/bytessrvd/logstash.conf > /opt/bytessrvd/logstash.log 2>&1 &
sleep 10
cd /opt/bytessrvd
. venv/bin/activate
python bytessrvd.py > /opt/bytessrvd/bytessrvd.log  2>&1 &

