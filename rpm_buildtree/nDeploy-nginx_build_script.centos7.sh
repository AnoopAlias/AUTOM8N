#!/bin/bash
#Author: Anoop P Alias

##Vars
NGINX_VERSION="1.10.1"
NGINX_RPM_ITER="2.el7"
NPS_VERSION="1.11.33.0"
MY_RUBY_VERSION="2.3.0"
PASSENGER_VERSION="5.0.28"
CACHE_PURGE_VERSION="2.3"
NAXSI_VERSION="0.55rc2"
OPENSSL_VERSION="1.0.2h"

rm -f nginx-pkg-64-centos7/nginx-nDeploy*
rm -rf nginx-${NGINX_VERSION}*

rsync -av --exclude 'etc/rc.d' nginx-pkg-64-common/ nginx-pkg-64-centos7/

yum -y install rpm-build libcurl-devel pcre-devel git xz-devel

gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
\curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=${MY_RUBY_VERSION}
. /usr/local/rvm/scripts/rvm
rvm use ruby-${MY_RUBY_VERSION}
echo ${MY_RUBY_VERSION}
/usr/local/rvm/rubies/ruby-${MY_RUBY_VERSION}/bin/gem install passenger -v ${PASSENGER_VERSION}
/usr/local/rvm/rubies/ruby-${MY_RUBY_VERSION}/bin/gem install fpm

wget http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz
tar -xvzf nginx-${NGINX_VERSION}.tar.gz
cd nginx-${NGINX_VERSION}/

wget https://github.com/nbs-system/naxsi/archive/${NAXSI_VERSION}.tar.gz
tar -xvzf ${NAXSI_VERSION}.tar.gz
sed -i 's/hash_init.bucket_size = 512/hash_init.bucket_size = 2048/' naxsi-${NAXSI_VERSION}/naxsi_src/naxsi_utils.c
sed -i 's/hash_init.max_size  = 1024/hash_init.max_size  = 256000/' naxsi-${NAXSI_VERSION}/naxsi_src/naxsi_utils.c

wget http://labs.frickle.com/files/ngx_cache_purge-${CACHE_PURGE_VERSION}.tar.gz
tar -xvzf ngx_cache_purge-${CACHE_PURGE_VERSION}.tar.gz

wget https://github.com/pagespeed/ngx_pagespeed/archive/release-${NPS_VERSION}-beta.zip
unzip release-${NPS_VERSION}-beta.zip
cd ngx_pagespeed-release-${NPS_VERSION}-beta/
wget https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz
tar -xzvf ${NPS_VERSION}.tar.gz
cd ..

wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz
tar -zxf openssl-${OPENSSL_VERSION}.tar.gz

./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/etc/nginx/modules --with-openssl=./openssl-${OPENSSL_VERSION} --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error_log --http-log-path=/var/log/nginx/access_log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nobody --group=nobody --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --add-dynamic-module=naxsi-${NAXSI_VERSION}/naxsi_src --with-file-aio --with-threads --with-stream --with-stream_ssl_module --with-http_slice_module --with-ipv6 --with-http_v2_module --add-dynamic-module=ngx_pagespeed-release-${NPS_VERSION}-beta --add-dynamic-module=/usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/src/nginx_module --add-module=ngx_cache_purge-${CACHE_PURGE_VERSION} --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --with-ld-opt=-Wl,-E
make DESTDIR=./tempo install

git clone https://github.com/nbs-system/naxsi-rules.git
rsync -av naxsi-rules/*.rules ../nginx-pkg-64-centos7/etc/nginx/conf.d/
rsync -av naxsi-${NAXSI_VERSION}/naxsi_config/naxsi_core.rules ../nginx-pkg-64-centos7/etc/nginx/naxsi_core.rules
rm -rf ../nginx-pkg-64-centos7/usr/nginx/nxapi
rsync -av naxsi-${NAXSI_VERSION}/nxapi ../nginx-pkg-64-centos7/usr/nginx/
rsync -av ../nxapi.json ../nginx-pkg-64-centos7/usr/nginx/nxapi/
rsync -av tempo/usr/sbin ../nginx-pkg-64-centos7/usr/
rsync -av tempo/etc/nginx/modules ../nginx-pkg-64-centos7/etc/nginx/

sed -i "s/RUBY_VERSION/$MY_RUBY_VERSION/g" ../nginx-pkg-64-centos7/etc/nginx/conf.d/passenger.conf
sed -i "s/PASSENGER_VERSION/$PASSENGER_VERSION/g" ../nginx-pkg-64-centos7/etc/nginx/conf.d/passenger.conf
sed -i "s/RUBY_VERSION/$MY_RUBY_VERSION/g" ../nginx-pkg-64-centos7/usr/nginx/scripts/nginx-passenger-setup.sh
sed -i "s/PASSENGER_VERSION/$PASSENGER_VERSION/g" ../nginx-pkg-64-centos7/usr/nginx/scripts/nginx-passenger-setup.sh

rm -rf ../nginx-pkg-64-centos7/usr/nginx/buildout
cp -pvr /usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/buildout ../nginx-pkg-64-centos7/usr/nginx/buildout
cd ../nginx-pkg-64-centos7
mkdir -p var/cache/nginx/ngx_pagespeed
mkdir -p var/log/nginx
mkdir -p var/run

fpm -s dir -t rpm -C ../nginx-pkg-64-centos7 --vendor "PiServe Technologies" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m info@piserve.com -e --description "nDeploy custom nginx package" --url http://piserve.com --conflicts nginx -d zlib -d openssl -d pcre -d libcurl -d memcached --after-install ../after_nginx_install --before-remove ../after_nginx_uninstall --name nginx-nDeploy .
rsync -av nginx-nDeploy-* root@rpm.piserve.com:/home/rpmrepo/public_html/CentOS/7/x86_64/
