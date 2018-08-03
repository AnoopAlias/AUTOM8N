#!/bin/bash
ps aux | grep -v grep | grep "nginx -s reload" > /dev/null
if [ $? -ne 0 ];then
  /usr/sbin/nginx -s reload > /dev/null 2>&1
  echo '1 nDeploy::nginX::reload'
fi
