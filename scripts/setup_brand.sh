#!/usr/bin/env bash

echo -e '\n<em><strong>Uninstalling previous version from cPanel...</strong></em>'
/usr/local/cpanel/scripts/uninstall_plugin /opt/nDeploy/nDeploy_cp

echo -e '\n<em><strong>Uninstalling application from WHM...</strong></em>'
/usr/local/cpanel/bin/unregister_appconfig /opt/nDeploy/nDeploy_whm/xtendweb.conf

/opt/nDeploy/scripts/fix_branding.py

echo -e '\n<em><strong>Installing nDeploy plugin in cPanel...</strong></em>'
/usr/local/cpanel/scripts/install_plugin /opt/nDeploy/nDeploy_cp

echo -e '\n<em><strong>Installing nDeploy plugin in WHM (</strong></em>Registering as XtendWeb<em><strong>)...</strong></em>'
/usr/local/cpanel/bin/register_appconfig /opt/nDeploy/nDeploy_whm/xtendweb.conf
