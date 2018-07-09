#!/bin/bash
kill -s USR2 $(cat /var/run/nginx.pid)
sleep 25
kill -s WINCH $(cat /var/run/nginx.pid.oldbin)
kill -s QUIT $(cat /var/run/nginx.pid.oldbin)
kill -s HUP $(cat /var/run/nginx.pid)
echo -e '\e[93m Nginx binary in-place upgrade: OK \e[0m'
