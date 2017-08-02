#/bin/bash
#Author: Anoop P Alias


yum -y install autoconf automake curl gcc git libmnl-devel libuuid-devel lm-sensors make nc pkgconfig python python-psycopg2 PyYAML zlib-devel python-pip
pip install MySQL-python
curl -Ss 'https://raw.githubusercontent.com/firehol/netdata-demo-site/master/install-required-packages.sh' >/tmp/kickstart.sh && bash /tmp/kickstart.sh -i netdata-all

git clone https://github.com/firehol/netdata.git --depth=1
cd netdata
./netdata-installer.sh --install /opt


sed -i '/virtfs/d' /opt/netdata/etc/netdata/netdata.conf
