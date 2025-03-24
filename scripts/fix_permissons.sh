#!/usr/bin/env bash

for dir in $(cat /etc/userdatadomains|awk -F"==" \'{print $5}\')
do
  echo "*** Fixing permissions for document_root ${dir} ***"
  find "${dir}"/ -type f -exec chmod 644 {} \;
  find "${dir}"/ -type d -exec chmod 755 {} \;
  echo "***  Done..   ***"
done
  
