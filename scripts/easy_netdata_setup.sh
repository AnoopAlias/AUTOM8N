#/bin/bash
#Author: Anoop P Alias


yum -y install autoconf automake curl gcc git libmnl-devel libuuid-devel lm-sensors make nc pkgconfig python python-psycopg2 PyYAML zlib-devel python-pip
pip install MySQL-python
curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all

git clone https://github.com/firehol/netdata.git --depth=1
cd netdata
./netdata-installer.sh --install /opt

echo -e '\e[93m Please set a password for user netdata below \e[0m'

htpasswd -c /etc/nginx/conf.d/netdata.password netdata
chmod 400 /etc/nginx/conf.d/netdata.password
chown nobody /etc/nginx/conf.d/netdata.password


echo -e '\e[93m setting up nginx httpd and mysql monitoring \e[0m'
mysql -e "create user 'netdata'@'localhost';"
mysql -e "grant usage on *.* to 'netdata'@'localhost' with grant option;"
mysql -e "flush privileges;"

sed -i 's/stub_status/nginx_status/' /opt/netdata/etc/netdata/python.d/nginx.conf
sed -i 's/server-status/whm-server-status/' /opt/netdata/etc/netdata/python.d/apache.conf
sed -i 's/access_log/access_log_disabled/' /opt/netdata/etc/netdata/python.d/web_log.conf
sed -i 's/# bind to = \*/bind to = 127.0.0.1:19999/' /opt/netdata/etc/netdata/netdata.conf

service netdata restart

/opt/nDeploy/scripts/generate_default_vhost_config.py
nginx -s reload

echo -e "\e[93m You can access netdata at https://$(hostname)/netdata with user: netdata and password you set \e[0m"

echo -e "\e[93m Do not remove /root/netdata folder as it is required for software upgrade and uninstall \e[0m"
