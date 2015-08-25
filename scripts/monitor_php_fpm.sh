#!/bin/bash

check() {
	VER=$1
	URL=http://localhost:808/ping$1
	RESPONSE=`curl $URL 2>/dev/null`
	echo "[`date`] URL=$URL Response=$RESPONSE"
	if [ "$RESPONSE" != 'pong' ]; then
		/etc/init.d/ndeploy_backends restart
		check $1
	fi
}

check 5.3
check 5.4
check 5.5