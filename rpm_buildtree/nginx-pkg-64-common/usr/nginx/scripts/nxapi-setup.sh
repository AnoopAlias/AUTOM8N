#!/bin/bash
#Author: Anoop P Alias
yum -y install python-pip
pip install --upgrade pip
pip install -r /usr/nginx/nxapi/requirements.txt
yum -y install python-GeoIP.x86_64 python-geoip-geolite2.noarch python-pygeoip.noarch java-1.8.0-openjdk.x86_64
rpm --import https://packages.elastic.co/GPG-KEY-elasticsearch
cat << EOF > /etc/yum.repos.d/elasticsearch.repo
[elasticsearch-1.7]
name=Elasticsearch repository for 1.7.x packages
baseurl=http://packages.elastic.co/elasticsearch/1.7/centos
gpgcheck=1
gpgkey=http://packages.elastic.co/GPG-KEY-elasticsearch
enabled=1
EOF
yum -y install elasticsearch
systemctl enable elasticsearch || chkconfig elasticsearch on
systemctl start elasticsearch || service elasticsearch start
sleep 20
curl -XGET http://localhost:9200/
if [ $? -ne 0 ];then
    echo "There is a problem with ElasticSeach daemon setup.Aborting NXAPI setup."
    exit 1
else
    curl -XPUT 'http://localhost:9200/nxapi/'
    mv /usr/nginx/scripts/nxapi-learn.sh.disabled /usr/nginx/scripts/nxapi-learn.sh
    echo "NXAPI setup complete"
fi
