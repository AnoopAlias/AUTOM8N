#!/bin/bash

/usr/local/cpanel/scripts/uninstall_plugin /opt/nDeploy/nDeploy_cp
/usr/local/cpanel/bin/unregister_appconfig /opt/nDeploy/nDeploy_whm/xtendweb.conf

/opt/nDeploy/scripts/fix_branding.py

echo -e '\e[93m Installing XtendWeb plugin in cPanel \e[0m'
/usr/local/cpanel/scripts/install_plugin /opt/nDeploy/nDeploy_cp
echo -e '\e[93m Installing XtendWeb plugin in WHM \e[0m'
/usr/local/cpanel/bin/register_appconfig /opt/nDeploy/nDeploy_whm/xtendweb.conf
