#!/bin/bash
#Author: Anoop P Alias

NDEPLOY_VERSION="4.0"
RPM_ITERATION="1"

rm -f nDeploy-cluster-slave-pkg-centos7/nDeploy-*
rsync -av ../scripts/postfix_backupmx_setup.sh ../scripts/postfix_backupmx_update.sh ../scripts/easy_php_setup.sh ../scripts/init_backends.py ../scripts/update_backend.py nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/scripts/
rsync -av ../conf/php-fpm.conf nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/conf/
rsync -av nDeploy-pkg-centos7/usr/lib/systemd/system/ndeploy_backends.service  nDeploy-cluster-slave-pkg-centos7/usr/lib/systemd/system/ndeploy_backends.service

rm -f nDeploy-cluster-slave-pkg/nDeploy-*
rsync -av ../scripts/postfix_backupmx_setup.sh ../scripts/postfix_backupmx_update.sh ../scripts/easy_php_setup.sh ../scripts/init_backends.py ../scripts/update_backend.py nDeploy-cluster-slave-pkg/opt/nDeploy/scripts/
rsync -av ../conf/php-fpm.conf nDeploy-cluster-slave-pkg/opt/nDeploy/conf/
rsync -av nDeploy-pkg/etc/rc.d/init.d/ndeploy_backends nDeploy-cluster-slave-pkg/etc/rc.d/init.d/ndeploy_backends

cd nDeploy-cluster-slave-pkg-centos7
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-cluster-slave-pkg-centos7 --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el7 -d python-inotify -d nginx-nDeploy -d python-argparse -d PyYAML -d python-lxml -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cluster slave" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_ndeploy_cluster_slave_install --name nDeploy-cluster-slave .
rsync -av nDeploy-* root@gnusys.net:/usr/share/nginx/html/CentOS/7/x86_64/
cd ..

cd nDeploy-cluster-slave-pkg
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-cluster-slave-pkg --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el6 -d python-inotify -d nginx-nDeploy -d python-argparse -d PyYAML -d python-lxml -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cluster slave" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_ndeploy_cluster_slave_install --name nDeploy-cluster-slave .
rsync -av nDeploy-* root@gnusys.net:/usr/share/nginx/html/CentOS/6/x86_64/
cd ..
