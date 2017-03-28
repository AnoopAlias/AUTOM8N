#!/bin/bash
#Author: Anoop P Alias


/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jailapache value=1
/usr/local/cpanel/bin/whmapi1 set_tweaksetting key=jaildefaultshell value=1
touch /opt/nDeploy/conf/chroot-php-enabled
