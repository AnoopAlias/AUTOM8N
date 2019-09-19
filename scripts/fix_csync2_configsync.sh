#!/bin/bash
#Author: Anoop P Alias

ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a "find /var/lib/csync2/ -type f -delete"
find /var/lib/csync2/ -type f -delete
ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a "csync2 -cIr /"
csync2 -cIr /
csync2 -TUXI
csync2 -fr /
csync2 -xr /
