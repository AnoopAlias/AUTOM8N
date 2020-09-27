#/bin/bash
#Author: Anoop P Alias

rpm -Uvh https://repository.pentestit.ru/nw/centos/nwaf-release-centos-7-1-6.noarch.rpm
# Keeping the repo disabled by default
yum-config-manager --disable NemesidaWAF
export TMPDIR=/root/tmp
yum -y --enablerepo=NemesidaWAF install nwaf-dyn-1.19
yum -y --enablerepo=ndeploy install nginx-nDeploy-module-nemesida
echo 'Setup: Ok'
