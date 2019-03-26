#!/bin/bash
mysql -e "SHOW SLAVE STATUS\G"|grep Relay_Master_Log_File|cut -d: -f2|sed 's/ //' > /home/mysql.status
