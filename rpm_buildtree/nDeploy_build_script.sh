#!/bin/bash
#Author: Anoop P Alias

NDEPLOY_VERSION="4.3"
RPM_ITERATION="44"

yum install gcc-c++ flex bison yajl yajl-devel curl-devel curl GeoIP-devel doxygen zlib-devel pcre-devel rpm-build

rm -f nDeploy-pkg/nDeploy-* nDeploy-pkg-centos7/nDeploy-*
rsync -av ../scripts/ nDeploy-pkg/opt/nDeploy/scripts/
rsync -av ../scripts/ nDeploy-pkg-centos7/opt/nDeploy/scripts/
rsync -av ../conf/ nDeploy-pkg/opt/nDeploy/conf/
rsync -av ../conf/ nDeploy-pkg-centos7/opt/nDeploy/conf/
rsync -av ../nDeploy_cp/ nDeploy-pkg/opt/nDeploy/nDeploy_cp/
rsync -av ../nDeploy_cp/ nDeploy-pkg-centos7/opt/nDeploy/nDeploy_cp/
rsync -av ../PHPfpmSelector/ nDeploy-pkg/opt/nDeploy/PHPfpmSelector/
rsync -av ../PHPfpmSelector/ nDeploy-pkg-centos7/opt/nDeploy/PHPfpmSelector/


cd nDeploy-pkg
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-pkg --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el6 -d python-psutil -d python-inotify -d python-jinja2 -d python-simplejson -d python-argparse -d PyYAML -d python-lxml -d python-configparser -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cPanel plugin" --url http://anoopalias.github.io/XtendWeb/ --before-install ../before_ndeploy_install --after-install ../after_ndeploy_install --before-remove ../after_ndeploy_uninstall --name nDeploy .
rsync -av nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/6/x86_64/

cd ..
cd nDeploy-pkg-centos7
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-pkg-centos7 --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el7 -d python-psutil -d python-inotify -d python-jinja2 -d python-simplejson -d python-argparse -d PyYAML -d python-lxml -d python-configparser -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cPanel plugin" --url http://anoopalias.github.io/XtendWeb/ --before-install ../before_ndeploy_install --after-install ../after_ndeploy_install --before-remove ../after_ndeploy_uninstall --name nDeploy .
rsync -av nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
cd ..
