#!/bin/bash
#Author: Anoop P Alias

VERSION="1"
RPM_ITERATION="4"

rm -f gnusys-monitoring/gnusys-monitoring-*
cd gnusys-monitoring
fpm -s dir -t rpm -C ../gnusys-monitoring --vendor "Anoop P Alias" --version ${VERSION} --iteration ${RPM_ITERATION}.el7 -d check-mk-agent -a noarch -m anoopalias01@gmail.com -e --description "GNUSYS monitoring plugin" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_gnusys_monitoring_install --name gnusys-monitoring .
rsync -av gnusys-monitoring-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
cd ..


rm -f gnusys-monitoring/gnusys-monitoring-*
cd gnusys-monitoring
fpm -s dir -t rpm -C ../gnusys-monitoring --vendor "Anoop P Alias" --version ${VERSION} --iteration ${RPM_ITERATION}.el6 -d check-mk-agent -a noarch -m anoopalias01@gmail.com -e --description "GNUSYS monitoring plugin" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_gnusys_monitoring_install --name gnusys-monitoring .
rsync -av gnusys-monitoring-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/6/x86_64/
cd ..
