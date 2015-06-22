#!/bin/sh

#if [ $1 -eq 0 ];then
	echo -e '\e[93m Removing cpanel stats processing hooks \e[0m'
	/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
	/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual
	/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountmodify_hook_pre.py --category Whostmgr --event Accounts::Modify --stage pre --manual
	/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountmodify_hook_post.py --category Whostmgr --event Accounts::Modify --stage post --manual
	/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountremove_hook_pre.py --category Whostmgr --event Accounts::Remove --stage pre --manual
#fi