#!/bin/bash
#Author: Anoop P Alias
yum -y install python-pip
pip install --upgrade pip
pip install -r /usr/nginx/nxapi/requirements.txt
yum -y install python-GeoIP.x86_64 python-geoip-geolite2.noarch python-pygeoip.noarch
echo "NXAPI setup in /usr/nginx/nxapi//usr/nginx/nxapi/"
