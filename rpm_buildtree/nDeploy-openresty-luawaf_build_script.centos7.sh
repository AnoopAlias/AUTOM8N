#!/bin/bash
#Author: Anoop P Alias

##Vars
LUARESTYWAF_VERSION="0.11"
LUARESTYWAF_RPM_ITER="1.el7"

rm -rf lua-resty-waf*


git clone https://github.com/p0pr0ck5/lua-resty-waf.git
cd lua-resty-waf
git submodule init
git submodule update
sed -i 's/^LUA_INCLUDE_DIR.*/LUA_INCLUDE_DIR=\/etc\/nginx\/luajit\/include\/luajit-2.1/' lua-aho-corasick/Makefile
make
install -d tempo/etc/nginx/site/lualib/resty/waf/storage
install -d tempo/etc/nginx/site/lualib/rules
install -m 644 lib/resty/*.lua tempo/etc/nginx/site/lualib/resty/
install -m 644 lib/resty/waf/*.lua tempo/etc/nginx/site/lualib/resty/waf/
install -m 644 lib/resty/waf/storage/*.lua tempo/etc/nginx/site/lualib/resty/waf/storage/
install -m 644 lib/*.so tempo/etc/nginx/site/lualib
install -m 644 rules/*.json tempo/etc/nginx/site/lualib/rules/
install -m 644 ../lua-resty-waf/luarestywaf.conf tempo/etc/nginx/conf.auto/
install -m 644 ../lua-resty-waf/luarestywaf_exec.conf tempo/etc/nginx/conf.d/
cd tempo
fpm -s dir -t rpm -C ../tempo --vendor "Anoop P Alias" --version ${LUARESTYWAF_VERSION} --iteration ${LUARESTYWAF_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom lua-resty-waf package" --url https://github.com/p0pr0ck5/lua-resty-waf -d openresty-nDeploy --name openresty-nDeploy-luarestywaf .
rsync -av openresty-nDeploy-luarestywaf* root@gnusys.net:/usr/share/nginx/html/CentOS/7/x86_64/
