#!/bin/bash
#Author: Anoop P Alias

RPM_ITERATION="40"

rm -f nDeploy-pkg/nDeploy-* nDeploy-pkg-centos7/nDeploy-*
rsync -av ../scripts/ nDeploy-pkg/opt/nDeploy/scripts/
rsync -av ../scripts/ nDeploy-pkg-centos7/opt/nDeploy/scripts/
rsync -av ../conf/ nDeploy-pkg/opt/nDeploy/conf/
rsync -av ../conf/ nDeploy-pkg-centos7/opt/nDeploy/conf/
rsync -av ../apache_fpm_cp/ nDeploy-pkg/opt/nDeploy/apache_fpm_cp/
rsync -av ../apache_fpm_cp/ nDeploy-pkg-centos7/opt/nDeploy/apache_fpm_cp/
rsync -av ../nDeploy_cp/ nDeploy-pkg/opt/nDeploy/nDeploy_cp/
rsync -av ../nDeploy_cp/ nDeploy-pkg-centos7/opt/nDeploy/nDeploy_cp/


cd nDeploy-pkg
mkdir lock
fpm -s dir -t rpm -C ../nDeploy-pkg --vendor "PiServe Technologies" --iteration ${RPM_ITERATION}.el6 -d python-inotify -d nginx-nDeploy -d python-argparse -d PyYAML -d python-lxml -a noarch -m info@piserve.com -e --description "nDeploy cPanel plugin" --url http://piserve.com --after-install ../after_ndeploy_install --before-remove ../after_ndeploy_uninstall --name nDeploy .

cd ..
cd nDeploy-pkg-centos7
mkdir lock
fpm -s dir -t rpm -C ../nDeploy-pkg-centos7 --vendor "PiServe Technologies" --iteration ${RPM_ITERATION}.el7 -d python-inotify -d nginx-nDeploy -d python-argparse -d PyYAML -d python-lxml -a noarch -m info@piserve.com -e --description "nDeploy cPanel plugin" --url http://piserve.com --after-install ../after_ndeploy_install --before-remove ../after_ndeploy_uninstall --name nDeploy .
cd ..
