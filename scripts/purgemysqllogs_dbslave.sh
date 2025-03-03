#!/usr/bin/env bash
myariadb -e "SHOW SLAVE STATUS\G"|grep Relay_Master_Log_File|cut -d: -f2|sed 's/ //' > /var/lib/maxscale/mysql.status
