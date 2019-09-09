#/bin/bash
#Author: Anoop P Alias


yum -y install MySQL-python iproute autoconf automake curl gcc git libmnl-devel libuuid-devel lm-sensors make nc nmap-ncat pkgconfig python python-psycopg2 PyYAML zlib-devel python-pip

### netdata compile from source ###
# curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all

# git clone https://github.com/firehol/netdata.git --depth=1
# cd netdata
# ./netdata-installer.sh --install /opt
### netdata compile from source ###

### netdata static build ###
bash <(curl -Ss https://my-netdata.io/kickstart-static64.sh)
### netdata static build ###

if [ ! -f /etc/nginx/conf.d/netdata.password ]; then

  if [ $# -ne 1 ];then

    echo -e '\e[93m Please set a password for user netdata below \e[0m'

    printf "netdata:$(openssl passwd -apr1)" > /etc/nginx/conf.d/netdata.password
    chmod 400 /etc/nginx/conf.d/netdata.password
    chown nobody /etc/nginx/conf.d/netdata.password
  else

    echo "netdata:$(openssl passwd -apr1 ${$1})" > /etc/nginx/conf.d/netdata.password
  fi
fi

conflineno=$(wc -l /opt/netdata/etc/netdata/netdata.conf|awk '{print $1}')

if [ ${conflineno} -lt 10 ];then
  wget -O /opt/netdata/etc/netdata/netdata.conf http://127.0.0.1:19999/netdata.conf
  sed -i '/\[health\]/aenabled = no' /opt/netdata/etc/netdata/netdata.conf
  sed -i 's/# enable by default cgroups matching =/enable by default cgroups matching = !lve*/' /opt/netdata/etc/netdata/netdata.conf
  sed -i 's/# bind to = \*/bind to = 127.0.0.1:19999/' /opt/netdata/etc/netdata/netdata.conf
fi

echo -e '\e[93m setting up nginx httpd and mysql monitoring \e[0m'
mysql -e "create user 'netdata'@'localhost';"
mysql -e "grant usage on *.* to 'netdata'@'localhost' with grant option;"
mysql -e "flush privileges;"

sed 's/stub_status/nginx_status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/nginx.conf > /opt/netdata/etc/netdata/python.d/nginx.conf
sed 's/\/server-status/\/whm-server-status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/apache.conf > /opt/netdata/etc/netdata/python.d/apache.conf
sed 's/\/access_log/\/access_log_disabled/' /opt/netdata/usr/lib/netdata/conf.d/python.d/web_log.conf > /opt/netdata/etc/netdata/python.d/web_log.conf

service netdata restart

if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
  /opt/nDeploy/scripts/generate_default_vhost_config.py
else
  /opt/nDeploy/scripts/generate_default_vhost_config_slave.py
fi

nginx -s reload

echo -e "\e[93m You can access netdata at https://$(hostname)/netdata with user: netdata and password you set \e[0m"
