#!/usr/bin/env bash
mysql -e "PURGE BINARY LOGS TO '$(cat /home/mysql.status)';" 2> /dev/null
