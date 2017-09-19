#!/bin/bash
#Author: Anoop P Alias

NDEPLOY_VERSION="4.3"
RPM_ITERATION="33"

rm -f nDeploy-cluster-slave-pkg-centos7/nDeploy-*
rsync -av ../scripts/easy_netdata_setup.sh ../scripts/setup_additional_templates.sh ../scripts/generate_default_vhost_config_slave.py ../scripts/easy_php_setup.sh ../scripts/easy_hhvm_setup.sh ../scripts/*ghost_hunter* ../scripts/init_backends.py ../scripts/update_backend.py nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/scripts/
rsync -av ../conf/php-fpm* ../conf/cpanel_services.conf.j2 ../conf/proxy_subdomain.conf.j2 ../conf/default_server.conf.j2 ../conf/hhvm* ../conf/httpd_mod_remoteip.include.j2 ../conf/secure-php-fpm* nDeploy-cluster-slave-pkg-centos7/opt/nDeploy/conf/
rsync -av nDeploy-pkg-centos7/usr/lib/systemd/system/ndeploy_backends.service  nDeploy-cluster-slave-pkg-centos7/usr/lib/systemd/system/ndeploy_backends.service

rm -f nDeploy-cluster-slave-pkg/nDeploy-*
rsync -av ../scripts/easy_netdata_setup.sh ../scripts/setup_additional_templates.sh ../scripts/generate_default_vhost_config_slave.py ../scripts/easy_php_setup.sh ../scripts/easy_hhvm_setup.sh ../scripts/*ghost_hunter* ../scripts/init_backends.py ../scripts/update_backend.py nDeploy-cluster-slave-pkg/opt/nDeploy/scripts/
rsync -av ../conf/php-fpm* ../conf/cpanel_services.conf.j2 ../conf/proxy_subdomain.conf.j2 ../conf/default_server.conf.j2 ../conf/hhvm* ../conf/httpd_mod_remoteip.include.j2 ../conf/secure-php-fpm* nDeploy-cluster-slave-pkg/opt/nDeploy/conf/
rsync -av nDeploy-pkg/etc/rc.d/init.d/ndeploy_backends nDeploy-cluster-slave-pkg/etc/rc.d/init.d/ndeploy_backends

cd nDeploy-cluster-slave-pkg-centos7
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-cluster-slave-pkg-centos7 --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el7 -d python-inotify -d python-argparse -d PyYAML -d python-lxml -d python-jinja2 -d python-simplejson -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cluster slave" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_ndeploy_cluster_slave_install --name nDeploy-cluster-slave .
rsync -av nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
cd ..

cd nDeploy-cluster-slave-pkg
mkdir opt/nDeploy/lock
fpm -s dir -t rpm -C ../nDeploy-cluster-slave-pkg --vendor "Anoop P Alias" --version ${NDEPLOY_VERSION} --iteration ${RPM_ITERATION}.el6 -d python-inotify -d python-argparse -d PyYAML -d python-lxml -d python-jinja2 -d python-simplejson -a noarch -m anoopalias01@gmail.com -e --description "nDeploy cluster slave" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_ndeploy_cluster_slave_install --name nDeploy-cluster-slave .
rsync -av nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/6/x86_64/
cd ..
