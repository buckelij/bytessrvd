##install virtualenv, java
sudo apt-get install openjdk-7-jre-headless
sudo apt-get install python-virtualenv

sudo useradd bytessrvd
chown -R bytessrvd /opt/bytessrvd
cd /opt/bytessrvd
sudo cp bytessrvd.conf /etc/init/
sudo chown root:root /etc/init/bytessrvd.conf

virtualenv venv
. venv/bin/activate
pip install Flask
curl -O https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.1.0.tar.gz
tar xvfz  elasticsearch-1.1.0.tar.gz
mv elasticsearch-1.1.0 elasticsearch
curl -O https://download.elasticsearch.org/logstash/logstash/logstash-1.4.0.tar.gz
tar xvfz logstash-1.4.0.tar.gz
mv logstash-1.4.0 logstash
