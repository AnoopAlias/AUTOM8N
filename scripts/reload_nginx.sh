#!/bin/bash
kill -USR1 $(cat /var/run/nginx.pid)
echo '1 nDeploy::nginX::USR1'
