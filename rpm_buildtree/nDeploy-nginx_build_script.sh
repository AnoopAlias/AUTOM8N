#!/bin/bash
#Author: Anoop P Alias

##Vars
#expecting 6/7 as the first arg to this scripts
#no sanitation is done as this would be mostly used by a person who knows what he is doing
OSVERSION=$1
NGINX_VERSION="1.12.0"
NGINX_RPM_ITER="4.el${OSVERSION}"
NPS_VERSION="1.12.34.2-stable"
MY_RUBY_VERSION="2.3.1"
PASSENGER_VERSION="5.1.5"
CACHE_PURGE_VERSION="2.3"
NAXSI_VERSION="http2"
PS_NGX_EXTRA_FLAGS="--with-cc=/opt/rh/devtoolset-2/root/usr/bin/gcc"
OPENSSL_VERSION="1.0.2k"
LIBRESSL_VERSION="2.5.2"
SRCACHE_NGINX_MODULE="0.31"
NGX_DEVEL_KIT="0.3.0"
REDIS2_NGINX_MODULE="0.13"
SET_MISC_NGINX_MODULE="0.31"
REDIS_NGINX_MODULE="0.3.8"
HEADERS_MORE_NGINX_MODULE="0.32"
ECHO_NGINX_MODULE="0.60"
PCRE_VERSION="8.40"
ZLIB_VERSION="1.2.11"



rm -rf nginx-module-*
rm -rf nginx-pkg
rm -rf nginx-${NGINX_VERSION}*
mkdir -p nginx-pkg/etc/nginx/{modules,modules.d,modules.debug,modules.debug.d,conf.auto}
mkdir -p nginx-pkg/usr/nginx/scripts
mkdir -p nginx-pkg/var/cache/nginx/ngx_pagespeed
mkdir -p nginx-pkg/var/log/nginx
mkdir -p nginx-pkg/var/run

for module in brotli geoip naxsi pagespeed passenger redis redis2 set_misc srcache_filter echo modsecurity testcookie_access
do
  mkdir -p nginx-module-${module}-pkg/etc/nginx/{modules,modules.d,modules.debug,modules.debug.d,conf.auto,conf.d}
  mkdir -p nginx-module-${module}-pkg/usr/nginx/scripts
done
mkdir -p nginx-module-naxsi-pkg/etc/nginx/naxsi.d

yum --enablerepo=ndeploy -y install rpm-build libcurl-devel git xz-devel GeoIP-devel libmodsecurity-nDeploy
if [ ${OSVERSION} -eq 6 ];then
  rpm --import https://linux.web.cern.ch/linux/scientific6/docs/repository/cern/slc6X/i386/RPM-GPG-KEY-cern
  wget -O /etc/yum.repos.d/slc6-devtoolset.repo https://linux.web.cern.ch/linux/scientific6/docs/repository/cern/devtoolset/slc6-devtoolset.repo
  yum install devtoolset-2-gcc-c++ devtoolset-2-binutils
  rsync -a --exclude 'usr/lib' --exclude 'etc/nginx/conf.d/modsecurity*' --exclude 'etc/nginx/naxsi.d/*' --exclude 'usr/nginx/scripts/*' --exclude 'etc/nginx/conf.d/naxsi_*' --exclude 'etc/nginx/conf.d/brotli.conf' --exclude 'etc/nginx/conf.d/pagespeed.conf' --exclude 'etc/nginx/conf.d/pagespeed_passthrough.conf' --exclude 'etc/nginx/fastcgi_params_geoip' --exclude 'etc/nginx/conf.auto/*' --exclude 'etc/nginx/modules.debug/*' --exclude 'etc/nginx/modules.debug.d/*' --exclude 'etc/nginx/modules/*' --exclude 'etc/nginx/modules.d/*' nginx-pkg-64-common/ nginx-pkg/
else
  rsync -a --exclude 'etc/rc.d' --exclude 'etc/nginx/conf.d/modsecurity*' --exclude 'etc/nginx/naxsi.d/*' --exclude 'usr/nginx/scripts/*' --exclude 'etc/nginx/conf.d/naxsi_*' --exclude 'etc/nginx/conf.d/brotli.conf' --exclude 'etc/nginx/conf.d/pagespeed.conf' --exclude 'etc/nginx/conf.d/pagespeed_passthrough.conf' --exclude 'etc/nginx/fastcgi_params_geoip' --exclude 'etc/nginx/conf.auto/*' --exclude 'etc/nginx/modules.debug/*' --exclude 'etc/nginx/modules.debug.d/*' --exclude 'etc/nginx/modules/*' --exclude 'etc/nginx/modules.d/*' nginx-pkg-64-common/ nginx-pkg/
fi


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

#test-cookie module
git clone https://github.com/kyprizel/testcookie-nginx-module.git

# ngx_cache_purge project is mostly unmaintained ;ignoring
#wget http://labs.frickle.com/files/ngx_cache_purge-${CACHE_PURGE_VERSION}.tar.gz
#tar -xvzf ngx_cache_purge-${CACHE_PURGE_VERSION}.tar.gz

# Pagespeed and brotli from google
#wget https://github.com/pagespeed/ngx_pagespeed/archive/release-${NPS_VERSION}-beta.zip
#unzip release-${NPS_VERSION}-beta.zip
#cd ngx_pagespeed-release-${NPS_VERSION}-beta/
#wget https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz
#tar -xzvf ${NPS_VERSION}.tar.gz
wget https://github.com/pagespeed/ngx_pagespeed/archive/v${NPS_VERSION}.zip
unzip v${NPS_VERSION}.zip
cd ngx_pagespeed-${NPS_VERSION}/
NPS_RELEASE_NUMBER=${NPS_VERSION/beta/}
NPS_RELEASE_NUMBER=${NPS_VERSION/stable/}
psol_url=https://dl.google.com/dl/page-speed/psol/${NPS_RELEASE_NUMBER}.tar.gz
[ -e scripts/format_binary_url.sh ] && psol_url=$(scripts/format_binary_url.sh PSOL_BINARY_URL)
wget ${psol_url}
tar -xzvf $(basename ${psol_url})  # extracts to psol/
cd ..

git clone https://github.com/google/ngx_brotli.git
cd ngx_brotli && git submodule update --init && cd ..

# LibreSSL , PCRE and ZLIB all latest versions
#wget https://www.openssl.org/source/openssl-${OPENSSL_VERSION}.tar.gz
#tar -zxf openssl-${OPENSSL_VERSION}.tar.gz

# LibreSSL
wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-${LIBRESSL_VERSION}.tar.gz
tar -zxf libressl-${LIBRESSL_VERSION}.tar.gz
cd libressl-${LIBRESSL_VERSION}
LIBRESSL_INSTALL_PATH=$(pwd)/.openssl
./configure LDFLAGS=-lrt --prefix=${LIBRESSL_INSTALL_PATH} && make install-strip
cd ..

# PCRE
wget https://ftp.pcre.org/pub/pcre/pcre-${PCRE_VERSION}.tar.gz
tar -zxf pcre-${PCRE_VERSION}.tar.gz

# ZLIB
wget http://zlib.net/zlib-${ZLIB_VERSION}.tar.gz
tar -zxf zlib-${ZLIB_VERSION}.tar.gz

# Modules from OpenResty project
wget -O srcache-nginx-module.tgz https://github.com/openresty/srcache-nginx-module/archive/v${SRCACHE_NGINX_MODULE}.tar.gz
wget -O ngx_devel_kit.tgz https://github.com/simpl/ngx_devel_kit/archive/v${NGX_DEVEL_KIT}.tar.gz
wget -O set-misc-nginx-module.tgz https://github.com/openresty/set-misc-nginx-module/archive/v${SET_MISC_NGINX_MODULE}.tar.gz
wget -O headers-more-nginx-module.tgz https://github.com/openresty/headers-more-nginx-module/archive/v${HEADERS_MORE_NGINX_MODULE}.tar.gz
#wget -O echo-nginx-module.tgz https://github.com/openresty/echo-nginx-module/archive/v${ECHO_NGINX_MODULE}.tar.gz
# To be removed later
git clone -b issue64 https://github.com/defanator/echo-nginx-module.git
mv echo-nginx-module echo-nginx-module-${ECHO_NGINX_MODULE}
wget http://people.freebsd.org/~osa/ngx_http_redis-${REDIS_NGINX_MODULE}.tar.gz
#wget -O redis2-nginx-module.tgz https://github.com/openresty/redis2-nginx-module/archive/v${REDIS2_NGINX_MODULE}.tar.gz
tar -xvzf ngx_http_redis-${REDIS_NGINX_MODULE}.tar.gz
tar -xvzf srcache-nginx-module.tgz
tar -xvzf ngx_devel_kit.tgz
tar -xvzf set-misc-nginx-module.tgz
tar -xvzf headers-more-nginx-module.tgz
tar -xvzf echo-nginx-module.tgz
#tar -xvzf redis2-nginx-module.tgz
git clone https://github.com/openresty/redis2-nginx-module.git

#libmodsecurity
# ensure env vars are set
export MODSECURITY_INC="/opt/nDeploy-libmodsecurity/include/"
export MODSECURITY_LIB="/opt/nDeploy-libmodsecurity/lib/"
git clone https://github.com/SpiderLabs/ModSecurity-nginx

if [ ${OSVERSION} -eq 6 ];then
./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/etc/nginx/modules --with-pcre=./pcre-${PCRE_VERSION} --with-pcre-jit --with-zlib=./zlib-${ZLIB_VERSION} --with-openssl=./libressl-${LIBRESSL_VERSION} --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error_log --http-log-path=/var/log/nginx/access_log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nobody --group=nobody --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --add-dynamic-module=naxsi-${NAXSI_VERSION}/naxsi_src --with-file-aio --with-threads --with-stream --with-stream_ssl_module --with-http_slice_module  --with-compat --with-http_v2_module --with-http_geoip_module=dynamic --add-dynamic-module=ngx_pagespeed-${NPS_VERSION} ${PS_NGX_EXTRA_FLAGS} --add-dynamic-module=/usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/src/nginx_module --add-dynamic-module=ngx_brotli --add-dynamic-module=echo-nginx-module-${ECHO_NGINX_MODULE} --add-dynamic-module=headers-more-nginx-module-${HEADERS_MORE_NGINX_MODULE} --add-dynamic-module=ngx_http_redis-${REDIS_NGINX_MODULE} --add-dynamic-module=redis2-nginx-module --add-dynamic-module=srcache-nginx-module-${SRCACHE_NGINX_MODULE} --add-dynamic-module=ngx_devel_kit-${NGX_DEVEL_KIT} --add-dynamic-module=set-misc-nginx-module-${SET_MISC_NGINX_MODULE} --add-dynamic-module=testcookie-nginx-module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --with-ld-opt="-Wl,-E -lrt"
else
./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/etc/nginx/modules --with-pcre=./pcre-${PCRE_VERSION} --with-pcre-jit --with-zlib=./zlib-${ZLIB_VERSION} --with-openssl=./libressl-${LIBRESSL_VERSION} --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error_log --http-log-path=/var/log/nginx/access_log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nobody --group=nobody --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --add-dynamic-module=naxsi-${NAXSI_VERSION}/naxsi_src --with-file-aio --with-threads --with-stream --with-stream_ssl_module --with-http_slice_module --with-compat --with-http_v2_module --with-http_geoip_module=dynamic --add-dynamic-module=ngx_pagespeed-${NPS_VERSION} --add-dynamic-module=/usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/src/nginx_module --add-dynamic-module=ngx_brotli --add-dynamic-module=echo-nginx-module-${ECHO_NGINX_MODULE} --add-dynamic-module=headers-more-nginx-module-${HEADERS_MORE_NGINX_MODULE} --add-dynamic-module=ngx_http_redis-${REDIS_NGINX_MODULE} --add-dynamic-module=redis2-nginx-module --add-dynamic-module=srcache-nginx-module-${SRCACHE_NGINX_MODULE} --add-dynamic-module=ngx_devel_kit-${NGX_DEVEL_KIT} --add-dynamic-module=set-misc-nginx-module-${SET_MISC_NGINX_MODULE} --add-dynamic-module=testcookie-nginx-module --add-dynamic-module=ModSecurity-nginx --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --with-ld-opt="-Wl,-E"
fi
make DESTDIR=$(pwd)/tempostrip install
strip --strip-debug ./tempostrip/usr/sbin/nginx
rsync -a tempostrip/usr/sbin ../nginx-pkg/usr/
strip --strip-debug ./tempostrip/etc/nginx/modules/*.so

if [ ${OSVERSION} -eq 6 ];then
./configure --with-debug --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/etc/nginx/modules --with-pcre=./pcre-${PCRE_VERSION} --with-pcre-jit --with-zlib=./zlib-${ZLIB_VERSION} --with-openssl=./libressl-${LIBRESSL_VERSION} --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error_log --http-log-path=/var/log/nginx/access_log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nobody --group=nobody --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --add-dynamic-module=naxsi-${NAXSI_VERSION}/naxsi_src --with-file-aio --with-threads --with-stream --with-stream_ssl_module --with-http_slice_module  --with-compat --with-http_v2_module --with-http_geoip_module=dynamic --add-dynamic-module=ngx_pagespeed-${NPS_VERSION} ${PS_NGX_EXTRA_FLAGS} --add-dynamic-module=/usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/src/nginx_module --add-dynamic-module=ngx_brotli --add-dynamic-module=echo-nginx-module-${ECHO_NGINX_MODULE} --add-dynamic-module=headers-more-nginx-module-${HEADERS_MORE_NGINX_MODULE} --add-dynamic-module=ngx_http_redis-${REDIS_NGINX_MODULE} --add-dynamic-module=redis2-nginx-module --add-dynamic-module=srcache-nginx-module-${SRCACHE_NGINX_MODULE} --add-dynamic-module=ngx_devel_kit-${NGX_DEVEL_KIT} --add-dynamic-module=set-misc-nginx-module-${SET_MISC_NGINX_MODULE} --add-dynamic-module=testcookie-nginx-module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --with-ld-opt="-Wl,-E -lrt"
else
./configure --with-debug --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/etc/nginx/modules --with-pcre=./pcre-${PCRE_VERSION} --with-pcre-jit --with-zlib=./zlib-${ZLIB_VERSION} --with-openssl=./libressl-${LIBRESSL_VERSION} --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error_log --http-log-path=/var/log/nginx/access_log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nobody --group=nobody --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --add-dynamic-module=naxsi-${NAXSI_VERSION}/naxsi_src --with-file-aio --with-threads --with-stream --with-stream_ssl_module --with-http_slice_module --with-compat --with-http_v2_module --with-http_geoip_module=dynamic --add-dynamic-module=ngx_pagespeed-${NPS_VERSION} --add-dynamic-module=/usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/src/nginx_module --add-dynamic-module=ngx_brotli --add-dynamic-module=echo-nginx-module-${ECHO_NGINX_MODULE} --add-dynamic-module=headers-more-nginx-module-${HEADERS_MORE_NGINX_MODULE} --add-dynamic-module=ngx_http_redis-${REDIS_NGINX_MODULE} --add-dynamic-module=redis2-nginx-module --add-dynamic-module=srcache-nginx-module-${SRCACHE_NGINX_MODULE} --add-dynamic-module=ngx_devel_kit-${NGX_DEVEL_KIT} --add-dynamic-module=set-misc-nginx-module-${SET_MISC_NGINX_MODULE} --add-dynamic-module=testcookie-nginx-module --add-dynamic-module=ModSecurity-nginx --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic' --with-ld-opt="-Wl,-E"
fi
make DESTDIR=$(pwd)/tempo install
rsync -a tempo/usr/sbin/nginx ../nginx-pkg/usr/sbin/nginx-debug

git clone https://github.com/SpiderLabs/owasp-modsecurity-crs.git
rsync -a owasp-modsecurity-crs ../nginx-module-modsecurity-pkg/etc/nginx/
mv ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/crs-setup.conf.example ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/crs-setup.conf
mv ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
mv ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example ../nginx-module-modsecurity-pkg/etc/nginx/owasp-modsecurity-crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf
git clone https://github.com/nbs-system/naxsi-rules.git
rsync -a naxsi-rules/*.rules ../nginx-module-naxsi-pkg/etc/nginx/naxsi.d/
rsync -a naxsi-${NAXSI_VERSION}/naxsi_config/naxsi_core.rules ../nginx-module-naxsi-pkg/etc/nginx/naxsi.d/naxsi_core.rules
rsync -a naxsi-${NAXSI_VERSION}/nxapi ../nginx-module-naxsi-pkg/usr/nginx/
rsync -a ../nxapi.json ../nginx-module-naxsi-pkg/usr/nginx/nxapi/
rsync -a ../nginx-pkg-64-common/etc/nginx/fastcgi_params_geoip ../nginx-module-geoip-pkg/etc/nginx/
rsync -a ../nginx-pkg-64-common/etc/nginx/conf.d/pagespeed.conf ../nginx-module-pagespeed-pkg/etc/nginx/conf.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/conf.d/pagespeed_passthrough.conf ../nginx-module-pagespeed-pkg/etc/nginx/conf.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/conf.d/brotli.conf ../nginx-module-brotli-pkg/etc/nginx/conf.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/conf.d/naxsi_* ../nginx-module-naxsi-pkg/etc/nginx/conf.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/conf.d/modsecurity.conf ../nginx-module-modsecurity-pkg/etc/nginx/conf.d/

for module in brotli geoip naxsi pagespeed passenger redis redis2 set_misc srcache_filter echo modsecurity testcookie_access
do
  rsync -a tempostrip/etc/nginx/modules/ngx_http_${module}* ../nginx-module-${module}-pkg/etc/nginx/modules/
  rsync -a tempo/etc/nginx/modules/ngx_http_${module}* ../nginx-module-${module}-pkg/etc/nginx/modules.debug/
  if [ -f ../nginx-pkg-64-common/etc/nginx/conf.auto/${module}.conf ] ; then
    rsync -a ../nginx-pkg-64-common/etc/nginx/conf.auto/${module}.conf ../nginx-module-${module}-pkg/etc/nginx/conf.auto/
  fi
  rsync -a ../nginx-pkg-64-common/etc/nginx/modules.d/${module}.load ../nginx-module-${module}-pkg/etc/nginx/modules.d/
  rsync -a ../nginx-pkg-64-common/etc/nginx/modules.debug.d/${module}.load ../nginx-module-${module}-pkg/etc/nginx/modules.debug.d/
done
rsync -a tempostrip/etc/nginx/modules/ngx_pagespeed.so ../nginx-module-pagespeed-pkg/etc/nginx/modules/
rsync -a tempo/etc/nginx/modules/ngx_pagespeed.so ../nginx-module-pagespeed-pkg/etc/nginx/modules.debug/
rsync -a tempostrip/etc/nginx/modules/ndk_http_module.so ../nginx-pkg/etc/nginx/modules/
rsync -a tempo/etc/nginx/modules/ndk_http_module.so ../nginx-pkg/etc/nginx/modules.debug/
rsync -a ../nginx-pkg-64-common/etc/nginx/modules.d/ndk.load ../nginx-pkg/etc/nginx/modules.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/modules.debug.d/ndk.load ../nginx-pkg/etc/nginx/modules.debug.d/
rsync -a tempostrip/etc/nginx/modules/ngx_http_headers_more_filter_module.so ../nginx-pkg/etc/nginx/modules/
rsync -a tempo/etc/nginx/modules/ngx_http_headers_more_filter_module.so ../nginx-pkg/etc/nginx/modules.debug/
rsync -a ../nginx-pkg-64-common/etc/nginx/modules.d/headers_more_filter.load ../nginx-pkg/etc/nginx/modules.d/
rsync -a ../nginx-pkg-64-common/etc/nginx/modules.debug.d/headers_more_filter.load ../nginx-pkg/etc/nginx/modules.debug.d/
mv ../nginx-module-modsecurity-pkg/etc/nginx/modules.d/modsecurity.load ../nginx-module-modsecurity-pkg/etc/nginx/modules.d/zz_modsecurity.load
mv ../nginx-module-modsecurity-pkg/etc/nginx/modules.debug.d/modsecurity.load ../nginx-module-modsecurity-pkg/etc/nginx/modules.debug.d/zz_modsecurity.load

rsync -a ../nginx-pkg-64-common/usr/nginx/scripts/nginx-passenger* ../nginx-module-passenger-pkg/usr/nginx/scripts/
rsync -a ../nginx-pkg-64-common/usr/nginx/scripts/nxapi* ../nginx-module-naxsi-pkg/usr/nginx/scripts/
#We remove redis2 from redis package which gets copied due to file glob
rm -f ../nginx-module-redis-pkg/etc/nginx/modules/ngx_http_redis2_module.so
rm -f ../nginx-module-redis-pkg/etc/nginx/modules.debug/ngx_http_redis2_module.so

sed -i "s/RUBY_VERSION/$MY_RUBY_VERSION/g" ../nginx-module-passenger-pkg/etc/nginx/conf.auto/passenger.conf
sed -i "s/PASSENGER_VERSION/$PASSENGER_VERSION/g" ../nginx-module-passenger-pkg/etc/nginx/conf.auto/passenger.conf
sed -i "s/RUBY_VERSION/$MY_RUBY_VERSION/g" ../nginx-module-passenger-pkg/usr/nginx/scripts/nginx-passenger-setup.sh
sed -i "s/PASSENGER_VERSION/$PASSENGER_VERSION/g" ../nginx-module-passenger-pkg/usr/nginx/scripts/nginx-passenger-setup.sh

rsync -a /usr/local/rvm/gems/ruby-${MY_RUBY_VERSION}/gems/passenger-${PASSENGER_VERSION}/buildout ../nginx-module-passenger-pkg/usr/nginx/
cd ../nginx-pkg

fpm -s dir -t rpm -C ../nginx-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx --conflicts openresty-nDeploy --after-install ../after_nginx_install --before-remove ../after_nginx_uninstall --name nginx-nDeploy .
rsync -a nginx-nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/${OSVERSION}/x86_64/

for module in brotli geoip naxsi pagespeed passenger redis redis2 set_misc srcache_filter echo modsecurity testcookie_access
do
  cd ../nginx-module-${module}-pkg
  if [ ${module} == "brotli" ];then
    fpm -s dir -t rpm -C ../nginx-module-${module}-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx-${module} package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx-module-${module} -d nginx-nDeploy --name nginx-nDeploy-module-${module} .
  elif [ ${module} == "modsecurity" ];then
    if [ ${OSVERSION} -gt 6 ];then
      fpm -s dir -t rpm -C ../nginx-module-${module}-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx-${module} package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx-module-${module} -d libmodsecurity-nDeploy -d nginx-nDeploy --name nginx-nDeploy-module-${module} .
    fi
  elif [ ${module} == "geoip" ];then
    fpm -s dir -t rpm -C ../nginx-module-${module}-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx-${module} package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx-module-${module} -d GeoIP -d nginx-nDeploy --name nginx-nDeploy-module-${module} .
  elif [ ${module} == "pagespeed" ];then
    fpm -s dir -t rpm -C ../nginx-module-${module}-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx-${module} package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx-module-${module} -d redis -d nginx-nDeploy --name nginx-nDeploy-module-${module} .
  else
    fpm -s dir -t rpm -C ../nginx-module-${module}-pkg --vendor "Anoop P Alias" --version ${NGINX_VERSION} --iteration ${NGINX_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com --description "nDeploy custom nginx-${module} package" --url http://anoopalias.github.io/XtendWeb/ --conflicts nginx-module-${module} -d nginx-nDeploy --name nginx-nDeploy-module-${module} .
  fi
  rsync -a nginx-nDeploy-* root@autom8n.com:/usr/share/nginx/autom8n/CentOS/${OSVERSION}/x86_64/
done
