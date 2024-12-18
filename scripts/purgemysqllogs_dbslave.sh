#!/usr/bin/env bash
mysql -e "SHOW SLAVE STATUS\G"|grep Relay_Master_Log_File|cut -d: -f2|sed 's/ //' > /var/lib/maxscale/mysql.status
