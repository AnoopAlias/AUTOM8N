#!/bin/bash
#Author: Anoop P Alias
yum -y install python-pip
pip install --upgrade pip
pip install -r /usr/nginx/nxapi/requirements.txt
echo "NXAPI setup in /usr/nginx/nxapi//usr/nginx/nxapi/"
