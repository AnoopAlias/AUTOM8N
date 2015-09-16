#!/bin/bash
# Author: Anoop P Alias

function enable {

minorver=$(httpd -v|grep "Server version:"|awk '{print $3}'|awk -F'/' '{print $2}'|awk -F'.' '{print $2}')
patchlevel=$(httpd -v|grep "Server version:"|awk '{print $3}'|awk -F'/' '{print $2}'|awk -F'.' '{print $3}')

if [ $minorver -lt 4 -o $patchlevel -lt 10 ];then
    echo -e "Apache httpd version >= \e[93m 2.4.10 \e[0m required for this setup"
    echo "Please recompile Apache httpd using the EasyApache cPanel script"
    exit 1
else
    /usr/local/apache/bin/apachectl -l|grep mod_proxy_fcgi
    if [ $? -ne 0 ];then
        if [ -f /var/cpanel/easy/apache/rawopts/Apache2_4 ];then 
            grep 'enable-proxy-fcgi=static' /var/cpanel/easy/apache/rawopts/Apache2_4 || echo '--enable-proxy-fcgi=static' >> /var/cpanel/easy/apache/rawopts/Apache2_4
        else
            echo '--enable-proxy-fcgi=static' >> /var/cpanel/easy/apache/rawopts/Apache2_4
        fi
        echo -e "Apache was \e[93m not \e[0m compiled with \e[93m mod_proxy_fcgi \e[0m"
        echo "I have added this option to EasyApache . Please recompile Apache using EasyApache"
        echo "Rerun this script once EasyApache is complete"
        echo -e "Select \e[93m MPM event \e[0m for better apache performance"
    else
        if [ -f /var/cpanel/templates/apache2_4/vhost.local ];then
            sed -i '/DocumentRoot/ r /opt/nDeploy/conf/apache_vhost_include_php.tmpl' /var/cpanel/templates/apache2_4/vhost.local
        else
	    cp -p /var/cpanel/templates/apache2_4/vhost.default /var/cpanel/templates/apache2_4/vhost.local
            sed -i '/DocumentRoot/ r /opt/nDeploy/conf/apache_vhost_include_php.tmpl' /var/cpanel/templates/apache2_4/vhost.local
        fi
        if [ -f /var/cpanel/templates/apache2_4/ssl_vhost.local ];then
            sed -i '/DocumentRoot/ r /opt/nDeploy/conf/apache_vhost_include_php.tmpl' /var/cpanel/templates/apache2_4/ssl_vhost.local
        else
	    cp -p /var/cpanel/templates/apache2_4/ssl_vhost.default /var/cpanel/templates/apache2_4/ssl_vhost.local
            sed -i '/DocumentRoot/ r /opt/nDeploy/conf/apache_vhost_include_php.tmpl' /var/cpanel/templates/apache2_4/ssl_vhost.local
        fi
        python /opt/nDeploy/scripts/apache_default_php_setup.py
        for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
        do
            echo "ConfGen:: $CPANELUSER" && /opt/nDeploy/scripts/apache_php_config_generator.py $CPANELUSER
         done
	which cagefsctl && cagefsctl --force-update
        /scripts/rebuildhttpdconf
        /scripts/restartsrv httpd
    fi
fi
}



function disable {

sed -i '/#nDeploy#/,/#nDeploy#/d' /var/cpanel/templates/apache2_4/vhost.local
sed -i '/#nDeploy#/,/#nDeploy#/d' /var/cpanel/templates/apache2_4/ssl_vhost.local
rm -f /opt/nDeploy/conf/user_data.yaml.tmpl 
/scripts/rebuildhttpdconf
/scripts/restartsrv httpd

}


case "$1" in
        enable)
            enable
            ;;
         
        disable)
            disable
            ;;
        *)
            echo $"Usage: $0 {enable|disable}"
            exit 1
 
esac
