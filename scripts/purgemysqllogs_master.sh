#!/usr/bin/env bash
ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeploydbslave -m fetch -a "src=//var/lib/maxscale/mysql.status dest=/var/lib/maxscale/mysql.status flat=yes"
mariadb -e "PURGE BINARY LOGS TO '$(cat /var/lib/maxscale/mysql.status)';" 2> /dev/null
