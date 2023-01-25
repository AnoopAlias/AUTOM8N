#!/usr/bin/env bash
#Author: Anoop P Alias

yum -y install MySQL-python iproute autoconf automake curl gcc git libmnl-devel libuuid-devel lm-sensors make nc nmap-ncat pkgconfig python python-psycopg2 PyYAML zlib-devel python-pip

curl https://my-netdata.io/kickstart.sh > /tmp/netdata-kickstart.sh && sh /tmp/netdata-kickstart.sh

if [ ! -f /etc/nginx/conf.d/netdata.password ]; then

  if [ $# -ne 1 ]; then
    echo -e ' Please set a password for user netdata below '
    printf "netdata:$(openssl passwd -apr1)" > /etc/nginx/conf.d/netdata.password
  else
    echo "netdata:$(openssl passwd -apr1 $1)" > /etc/nginx/conf.d/netdata.password
  fi

fi

chmod 400 /etc/nginx/conf.d/netdata.password
chown nobody /etc/nginx/conf.d/netdata.password


conflineno=$(wc -l /etc/netdata/netdata.conf|awk '{print $1}')

if [ ${conflineno} -lt 40 ];then
  curl -o /etc/netdata/netdata.conf http://localhost:19999/netdata.conf
  sed -i '/\[health\]/aenabled = no' /etc/netdata/netdata.conf
  sed -i 's/# enable by default cgroups matching =/enable by default cgroups matching = !lve*/' /etc/netdata/netdata.conf
  sed -i 's/# bind to = \*/bind to = 127.0.0.1:19999/' /etc/netdata/netdata.conf
fi


echo -e ' setting up nginx httpd and mysql monitoring '
mysql -e "create user 'netdata'@'localhost';"
mysql -e "grant usage on *.* to 'netdata'@'localhost' with grant option;"
mysql -e "flush privileges;"

sed -i 's/\/server-status/\/whm-server-status/' /usr/lib/netdata/conf.d/go.d/apache.conf
sed -i 's/\/access_log/\/access_log_disabled/' /usr/lib/netdata/conf.d/go.d/web_log.conf

service netdata restart

if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
  /opt/nDeploy/scripts/generate_default_vhost_config.py
else
  /opt/nDeploy/scripts/generate_default_vhost_config_slave.py
fi

nginx -s reload

echo -e " You can access netdata at https://$(hostname)/netdata with user: netdata and password you set "
