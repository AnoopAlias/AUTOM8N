#!/bin/bash
#Author: Anoop P Alias

yum --enablerepo=ndeploy -y install openresty-nDeploy-luarestywaf openresty-nDeploy-luarocks

/etc/nginx/bin/opm get hamishforbes/lua-resty-iputils p0pr0ck5/lua-resty-cookie p0pr0ck5/lua-ffi-libinjection p0pr0ck5/lua-resty-logger-socket
/etc/nginx/luajit/bin/luarocks install lrexlib-pcre 2.7.2-1
/etc/nginx/luajit/bin/luarocks install busted
/etc/nginx/luajit/bin/luarocks install luafilesystem

echo -e '\e[93m OpenResty lua-resty-waf setup: OK \e[0m'
