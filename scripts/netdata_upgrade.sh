#/bin/bash
#Author: Anoop P Alias

rsync -av /opt/netdata/etc/netdata/netdata.conf /opt/netdata/etc/netdata/netdata.conf.backup
wget -O /root/kickstart-static64.sh https://my-netdata.io/kickstart-static64.sh && bash /root/kickstart-static64.sh --non-interactive
sed -i 's/stub_status/nginx_status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/nginx.conf
sed -i 's/\/server-status/\/whm-server-status/' /opt/netdata/usr/lib/netdata/conf.d/python.d/apache.conf
sed -i 's/\/access_log/\/access_log_disabled/' /opt/netdata/usr/lib/netdata/conf.d/python.d/web_log.conf
rsync -av /opt/netdata/etc/netdata/netdata.conf.backup /opt/netdata/etc/netdata/netdata.conf
service netdata restart
