#!/bin/bash
#Author: Anoop P Alias

NDEPLOY_VERSION="2.0"
RPM_ITERATION="5"

rm -f nDeploy-cluster-slave-pkg-centos7/nDeploy-*
rsync -av ../scripts/cluster_slave_setup_backends.py ../scripts/easy_php_setup.sh ../scripts/init_backends.py ../scripts/update_backend.py nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/scripts/
rsync -av ../conf/php-fpm.conf ../conf/php-fpm.pool.tmpl nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/conf/

cd nDeploy-cluster-slave-pkg-centos7
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-cluster-slave-pkg-centos7 --vendor "PiServe Technologies" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el7 -d python-inotify -d nginx-nDeploy -d python-argparse -d PyYAML -d python-lxml -a noarch -m info@piserve.com -e --description "nDeploy cluster slave" --url http://piserve.com --after-install ../after_ndeploy_cluster_slave_install --name nDeploy-cluster-slave .
cp nDeploy-* /home/rpmrepo/public_html/CentOS/7/x86_64/
cd ..
