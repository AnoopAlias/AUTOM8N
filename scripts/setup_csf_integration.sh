#!/usr/bin/env bash


function enable {
  if [ -f /etc/csf/csf.conf ] ; then
		sed -i 's/^CUSTOM8_LOG.*$/CUSTOM8_LOG = \"\/var\/log\/nginx\/error_log\"/' /etc/csf/csf.conf
    csf -r
	fi
}

function disable {
  if [ -f /etc/csf/csf.conf ] ; then
		sed -i 's/^CUSTOM8_LOG.*$/CUSTOM8_LOG = \"\/var\/log\/customlog\"/' /etc/csf/csf.conf
    csf -r
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
