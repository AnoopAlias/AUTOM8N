#!/bin/bash
#Author: Anoop P Alias
yum -y install python-pip
pip install --upgrade pip
pip install -r /usr/nginx/nxapi/requirements.txt
cd /usr/nginx/nxapi/
python setup.py install
