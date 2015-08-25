#!/bin/sh

yum install python-argparse PyYAML python-lxml incron -y

touch /opt/nDeploy/conf/backends.yaml
/opt/nDeploy/scripts/update_backend.py PROXY apache 8000
touch /opt/nDeploy/conf/profiles.yaml
/opt/nDeploy/scripts/update_profiles.py PROXY 1000 "Proxy to the Apache Backend (default)"
/opt/nDeploy/scripts/update_profiles.py NODEJS 4001 "A NodeJS application"
/opt/nDeploy/scripts/update_profiles.py NODEJS 4002 "Ghost Blog"
/opt/nDeploy/scripts/update_profiles.py RUBY 2001 "Rack or Ruby on Rails"
/opt/nDeploy/scripts/update_profiles.py PYTHON 3001 "Python WSGI Application"
/opt/nDeploy/scripts/update_profiles.py PHP 5001 "Wordpress or Drupal"
/opt/nDeploy/scripts/update_profiles.py PHP 5002 "Joomla"
/opt/nDeploy/scripts/update_profiles.py PHP 5003 "Magento"

echo -e '\e[93m Adding cpanel hooks \e[0m'
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountcreate_hook_post.pl --category Whostmgr --event Accounts::Create --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountmodify_hook_pre.py --category Whostmgr --event Accounts::Modify --stage pre --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountmodify_hook_post.py --category Whostmgr --event Accounts::Modify --stage post --manual
/usr/local/cpanel/bin/manage_hooks delete script /opt/nDeploy/scripts/accountremove_hook_pre.py --category Whostmgr --event Accounts::Remove --stage pre --manual

/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunAll --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/reload_nginx.sh --category Stats --event RunUser --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountcreate_hook_post.pl --category Whostmgr --event Accounts::Create --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountmodify_hook_pre.py --category Whostmgr --event Accounts::Modify --stage pre --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountmodify_hook_post.py --category Whostmgr --event Accounts::Modify --stage post --manual
/usr/local/cpanel/bin/manage_hooks add script /opt/nDeploy/scripts/accountremove_hook_pre.py --category Whostmgr --event Accounts::Remove --stage pre --manual

if [ -z "$PHPBREW_ROOT" ] ; then
	export PHPBREW_ROOT=/usr/local/phpbrew
	echo "export PHPBREW_ROOT=/usr/local/phpbrew" >> /root/.bashrc
fi
if [ -z "$NVM_DIR" ] ; then
	export NVM_DIR="/usr/local/nvm"
	echo "export NVM_DIR=/usr/local/nvm" >> /root/.bashrc
fi
if [ ! -d /opt/nDeploy/domain-data ] ; then
	mkdir /opt/nDeploy/domain-data
fi

ln -s /opt/nDeploy/nDeploy_cp /usr/local/cpanel/base/frontend/x3/
ln -s /opt/nDeploy/nDeploy_cp /usr/local/cpanel/base/frontend/paper_lantern/
cp /opt/nDeploy/ndeploy_backends.init /etc/init.d/ndeploy_backends && chmod +x /etc/init.d/ndeploy_backends
cp /opt/nDeploy/ndeploy.incron /etc/incron.d/nDeploy && chmod +x /etc/init.d/ndeploy_backends
/usr/local/cpanel/scripts/install_plugin /opt/nDeploy/nDeploy_cp
/usr/local/cpanel/scripts/install_plugin /opt/nDeploy/nDeploy_cp --theme x3
for CPANELUSER in `cat /etc/domainusers|cut -d: -f1`; do
	/opt/nDeploy/scripts/generate_config.py $CPANELUSER
done
