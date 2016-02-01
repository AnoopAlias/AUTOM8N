#!/bin/bash
#Author : Anoop P Alias

function enable {
    if [ ! -f /etc/nginx/dos_protection_enabled ];then
        cp -p /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bkup.script
        rsync -av /etc/nginx/nginx.conf.ddos /etc/nginx/nginx.conf
        systemctl restart nginx || service nginx restart
        touch /etc/nginx/dos_protection_enabled
    else
        echo "DOS protection already enabled"
    fi
}
function disable {
    if [ -f /etc/nginx/dos_protection_enabled ];then
        rsync -av /etc/nginx/nginx.conf.bkup.script /etc/nginx/nginx.conf
        rm -f /etc/nginx/nginx.conf.bkup.script
        rm -f /etc/nginx/dos_protection_enabled
        systemctl restart nginx || service nginx restart
    else
        echo "DOS protection not enabled"
    fi
}

case "$1" in
        enable)
            enable
            ;;

        disable)
            disable
            ;;
        *)
            echo $"Usage: $0 {enable|disable}"
            exit 1

esac
