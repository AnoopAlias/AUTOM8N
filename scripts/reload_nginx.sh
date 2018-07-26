#!/bin/bash
/usr/sbin/nginx -s reload > /dev/null 2>&1
echo '1 nDeploy::nginX::reload'
