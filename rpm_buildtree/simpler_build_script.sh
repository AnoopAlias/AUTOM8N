#!/bin/bash
#Author: Anoop P Alias

NDEPLOY_VERSION="4.3"
RPM_ITERATION="38"

yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel pcre-devel rpm-build

rm -rf simpler
rsync -av ../simpler/ ./simpler/


cd simpler
fpm -s dir -t rpm -C ../simpler --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el7 -d nDeploy -a noarch -m anoopalias01@gmail.com -e --description "SimpleR WHM plugin" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_simpler_install --before-remove ../after_simpler_uninstall --name simpler-nDeploy .
rsync -av simpler-nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
cd ..
