#!/bin/bash
ps aux | grep -v grep | grep "nginx -s reload" > /dev/null
if [ $? -ne 0 ];then
  /usr/bin/kill -USR1 $(cat /var/run/nginx.pid)
  echo '1 nDeploy::nginX::reload'
fi
