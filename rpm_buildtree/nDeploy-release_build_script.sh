#!/bin/bash
#Author: Anoop P Alias

cd nDeploy-release-centos-pkg
fpm -s dir -t rpm -C ../nDeploy-release-centos-pkg --vendor "PiServe Technologies" --iteration 3 -a noarch -m info@piserve.com -e --description "nDeploy rpm repo" --url http://piserve.com --name nDeploy-release-centos .
cd ..
