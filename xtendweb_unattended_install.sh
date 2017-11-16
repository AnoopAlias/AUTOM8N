#!/bin/bash

echo -e '\e[93m Press Ctrl+c now if you havent purchased a license  \e[0m'
sleep 10

yum -y install epel-release
yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-6.noarch.rpm
yum -y --enablerepo=ndeploy install nginx-nDeploy nDeploy
if [ $? -eq 0 ];then
  /opt/nDeploy/scripts/easy_php_setup.sh
  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable
else
  echo -e '\e[93m Please purchase a license or contact ops@gnusys.net \e[0m'
fi
