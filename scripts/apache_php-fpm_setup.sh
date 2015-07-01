#!/bin/bash
# Author: Anoop P Alias

function enable {

myversion=$(httpd -v|grep "Server version:"|awk '{print $3}'|awk -F'/' '{print $2}')
testresult=$(echo "$myversion > 2.4.10"|bc)
if [ $testresult -ne 1 ];then
    echo "Apache httpd version >= 2.4.10 required for this setup"
    echo "Please recompile Apache httpd using the EasyApache cPanel script"
    exit 1
else
    if [ ! /usr/local/apache/bin/apachectl -l|grep mod_proxy_fcgi ];then

        if [ -f /var/cpanel/easy/apache/rawopts/Apache2_4 ];then 
            grep 'enable-proxy-fcgi=static' /var/cpanel/easy/apache/rawopts/Apache2_4 || echo '--enable-proxy-fcgi=static' >> /var/cpanel/easy/apache/rawopts/Apache2_4
        else
            echo '--enable-proxy-fcgi=static' >> /var/cpanel/easy/apache/rawopts/Apache2_4
        fi
        echo "Apache was not compiled with mod_proxy_fcgi"
        echo "I have added the option to EasyApache . Please recompile Apache using EasyApache"
        echo "Rerun this script once EasyApache is complete"
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
