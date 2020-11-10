#!/usr/bin/env bash

/usr/bin/kill -s SIGUSR1 $(cat /var/run/nginx.pid)
echo '1 nDeploy::nginX::reload'
