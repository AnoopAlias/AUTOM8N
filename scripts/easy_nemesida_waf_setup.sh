#!/usr/bin/env bash
#Author: Anoop P Alias

OSVERSION=$(cat /etc/redhat-release | grep -oE '[0-9]+\.[0-9]+'|cut -d"." -f1)
NGINX_MINOR_VERSION=$(rpm -qa|grep nginx-nDeploy|awk -F"." '{print $2}')

if [ ${OSVERSION} -eq 7 ];then
rpm -Uvh https://repository.pentestit.ru/nw/centos/nwaf-release-centos-7-1-6.noarch.rpm
# Keeping the repo disabled by default
yum-config-manager --disable NemesidaWAF
export TMPDIR=/root/tmp
pip3 install cython # https://forum.nemesida-security.com/threads/scikit-learn-dependency-error-for-cython-in-centos7-and-centos8.51/
yum -y --enablerepo=NemesidaWAF install nwaf-dyn-1.${NGINX_MINOR_VERSION}
yum -y --enablerepo=ndeploy install nginx-nDeploy-module-nemesida
rsync -av /opt/nDeploy/conf/nwaf.conf /etc/nginx/nwaf/conf/global/nwaf.conf
echo 'Setup: Ok'
elif [ ${OSVERSION} -eq 8 ];then
rpm -Uvh https://repository.pentestit.ru/nw/centos/nwaf-release-centos-8-1-6.noarch.rpm
# Keeping the repo disabled by default
yum-config-manager --disable NemesidaWAF
export TMPDIR=/root/tmp
pip3 install cython # https://forum.nemesida-security.com/threads/scikit-learn-dependency-error-for-cython-in-centos7-and-centos8.51/
# Setting up packagecloud.io for rabbitmq-server
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | sudo bash
yum -y --enablerepo=NemesidaWAF install nwaf-dyn-1.${NGINX_MINOR_VERSION}
yum -y --enablerepo=ndeploy install nginx-nDeploy-module-nemesida
rsync -av /opt/nDeploy/conf/nwaf.conf /etc/nginx/nwaf/conf/global/nwaf.conf
echo 'Setup: Ok'
else
echo "Setup: Failed"
fi
