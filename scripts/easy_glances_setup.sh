#!/bin/bash
#Author: Anoop P Alias

which systemctl || exit 1
yum -y remove glances
yum -y --enablerepo=epel install python36 python36-pip python36-devel
pip3 install glances bottle

if [ ! -f /etc/nginx/conf.d/glances.password ]; then

  if [ $# -ne 1 ]; then
    echo -e ' Please set a password for user glances below '
    printf "glances:$(openssl passwd -apr1)" > /etc/nginx/conf.d/glances.password
  else
    echo "glances:$(openssl passwd -apr1 $1)" > /etc/nginx/conf.d/glances.password
  fi

fi

chmod 400 /etc/nginx/conf.d/glances.password
chown nobody /etc/nginx/conf.d/glances.password

systemctl enable ndeploy_glances
systemctl start ndeploy_glances

if [ -d /opt/nDeploy/conf/nDeploy-cluster ];then
  /opt/nDeploy/scripts/generate_default_vhost_config.py
else
  /opt/nDeploy/scripts/generate_default_vhost_config_slave.py
fi

nginx -s reload

echo -e " You can access glances at https://$(hostname)/glances with user: glances and password you set "
