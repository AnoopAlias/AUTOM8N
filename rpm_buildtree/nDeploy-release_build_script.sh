#!/bin/bash
#Author: Anoop P Alias

cd nDeploy-release-centos-pkg
fpm -s dir -t rpm -C ../nDeploy-release-centos-pkg --vendor "Anoop P Alias" --iteration 6 -a noarch -m anoopalias01@gmail.com -e --description "nDeploy rpm repo" --url http://anoopalias.github.io/XtendWeb/ --after-install ../after_ndeploy_release_install --name nDeploy-release-centos .
cd ..
