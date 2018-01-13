#!/bin/bash

find /etc/systemd/system -iname limits.conf -exec rm -f {} \;
rm -f /etc/systemd/system/root.slice
for thereseller in $(cat /var/cpanel/resellers | cut -d":" -f1)
do
  rm -f /etc/systemd/system/${thereseller}.slice
done
systemctl daemon-reload
echo -e '\e[93m Removed SimpleR set files. You will be able to manage application/reseller limits from XtendWeb WHM plugin now \e[0m'
