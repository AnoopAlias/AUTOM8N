#!/bin/bash
#Author: Anoop P Alias

cd nDeploy-release-centos-pkg
fpm -s dir -t rpm -C ../nDeploy-release-centos-pkg --vendor "Anoop P Alias" --iteration 3 -a noarch -m anoopalias01@gmail.com -e --description "nDeploy rpm repo" --url http://anoopalias.github.io/nDeploy/ --name nDeploy-release-centos .
cd ..
