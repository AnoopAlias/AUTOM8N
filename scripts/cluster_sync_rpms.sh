#!/bin/bash

phprpms=$(rpm -qa|egrep '^ea-php'|sed 's/-[0-9].*//')
ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -a "yum -y install ${phprpms}"
echo -e '\e[93m In case you see errors remove conflicting RPMs on slave and rerun this script \e[0m'
