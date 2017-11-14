#!/bin/bash
#Author: Anoop P Alias

##Vars
MODSEC_VERSION="3.0"
MODSEC_RPM_ITER="13.el7"

rm -rf ModSecurity*
yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel pcre-devel rpm-build ssdeep*
git clone https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
git checkout -b v3/master origin/v3/master
sh build.sh
git submodule init
git submodule update
./configure -without-lmdb --prefix=/opt/nDeploy-libmodsecurity
make DESTDIR=$(pwd)/tempo install
cd tempo

fpm -s dir -t rpm -C ../tempo --vendor "Anoop P Alias" --version ${MODSEC_VERSION} --iteration ${MODSEC_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom libmodsecurity package" --url https://github.com/SpiderLabs/ModSecurity -d libcurl -d GeoIP -d yajl -d libxml2 -d ssdeep --name libmodsecurity-nDeploy .
rsync -av libmodsecurity-nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
