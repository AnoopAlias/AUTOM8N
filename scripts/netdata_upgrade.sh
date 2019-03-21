#/bin/bash
#Author: Anoop P Alias

wget -O /root/kickstart-static64.sh https://my-netdata.io/kickstart-static64.sh && bash /root/kickstart-static64.sh --non-interactive
service netdata restart
