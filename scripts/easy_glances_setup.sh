#/bin/bash
#Author: Anoop P Alias

which systemctl || exit 1
yum -y remove glances
yum -y --enablerepo=epel install python36 python36-pip python36-devel
pip3 install glances bottle

echo -e "\e[93m Input web user password for glances user below \e[0m"
printf "glances:$(openssl passwd -apr1)" > /etc/nginx/conf.d/glances.password
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

echo -e "\e[93m You can access glances at https://$(hostname)/glances with user: glances and password you set \e[0m"
