#/bin/bash
#Author: Anoop P Alias


yum -y install iproute autoconf automake curl gcc git libmnl-devel libuuid-devel lm-sensors make nc nmap-ncat pkgconfig python python-psycopg2 PyYAML zlib-devel python-pip
pip install MySQL-python

### netdata compile from source ###
# curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all

# git clone https://github.com/firehol/netdata.git --depth=1
# cd netdata
# ./netdata-installer.sh --install /opt
### netdata compile from source ###

### netdata static build ###
bash <(curl -Ss https://my-netdata.io/kickstart-static64.sh)
### netdata static build ###

echo -e '\e[93m Please set a password for user netdata below \e[0m'

printf "netdata:$(openssl passwd -apr1)" > /etc/nginx/conf.d/netdata.password
chmod 400 /etc/nginx/conf.d/netdata.password
chown nobody /etc/nginx/conf.d/netdata.password


wget -O /opt/netdata/etc/netdata/netdata.conf http://127.0.0.1:19999/netdata.conf
echo -e '\e[93m setting up nginx httpd and mysql monitoring \e[0m'
mysql -e "create user 'netdata'@'localhost';"
mysql -e "grant usage on *.* to 'netdata'@'localhost' with grant option;"
mysql -e "flush privileges;"

sed -i 's/stub_status/nginx_status/' /opt/netdata/etc/netdata/python.d/nginx.conf
sed -i 's/\/server-status/\/whm-server-status/' /opt/netdata/etc/netdata/python.d/apache.conf
sed -i 's/\/access_log/\/access_log_disabled/' /opt/netdata/etc/netdata/python.d/web_log.conf
sed -i 's/# bind to = \*/bind to = 127.0.0.1:19999/' /opt/netdata/etc/netdata/netdata.conf

sed -i 's/stub_status/nginx_status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/nginx.conf
sed -i 's/\/server-status/\/whm-server-status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/apache.conf
sed -i 's/\/access_log/\/access_log_disabled/' /opt/netdata/usr/lib/netdata/conf.d/python.d/web_log.conf

service netdata restart

if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
  /opt/nDeploy/scripts/generate_default_vhost_config.py
else
  /opt/nDeploy/scripts/generate_default_vhost_config_slave.py
fi

nginx -s reload

echo -e "\e[93m You can access netdata at https://$(hostname)/netdata with user: netdata and password you set \e[0m"
