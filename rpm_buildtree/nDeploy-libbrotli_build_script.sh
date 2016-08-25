#!/bin/bash
#Author: Anoop P Alias

##Vars
BROTLI_VERSION="1.0"
BROTLI_RPM_ITER="1.el6"

rm -rf /opt/libbrotli
git clone https://github.com/bagder/libbrotli
cd libbrotli
./autogen.sh
./configure --prefix=/usr --libdir=/usr/lib64
make DESTDIR=/opt/libbrotli install
cd /opt/libbrotli

fpm -s dir -t rpm -C ../libbrotli --vendor "Anoop P Alias" --version ${BROTLI_VERSION} --iteration ${BROTLI_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom libbrotli package" --url https://github.com/bagder/libbrotli --conflicts libbrotli --name libbrotli-nDeploy .
rsync -av libbrotli-nDeploy-* root@rpm.piserve.com:/home/gnusys/public_html/CentOS/6/x86_64/
