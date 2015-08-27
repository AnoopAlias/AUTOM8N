#!/bin/bash

check() {
	VER=$1
	URL=http://localhost:808/ping$1
	RESPONSE=`curl $URL 2>/dev/null`
	echo "[`date`] URL=$URL Response=$RESPONSE"
	if [ "$RESPONSE" != 'pong' ]; then
		/opt/nDeploy/scripts/init_backends.pl --action=restart --forced --php=$VER
	fi
}

#check 5.3
#check 5.4
#check 5.5