#!/usr/bin/env bash
  
: ${1?"Usage: $0 CPANELUSER"}
CPANELUSER="${1}"
if [ -f /var/cpanel/users/${CPANELUSER} ];then

HOMEDIR=$( getent passwd "${CPANELUSER}" | cut -d: -f6 )
if [ -d ${HOMEDIR} ]; then
  echo "*** Fixing ownership and group of account ${CPANELUSER} in home ${HOMEDIR}  ***"

  find ${HOMEDIR}/ -not \( -group ${CPANELUSER} -o -group nobody -o -group mail -o -group root -o -group mysql \) -print -exec chgrp ${CPANELUSER} {} \;
  find ${HOMEDIR}/ -not \( -user ${CPANELUSER} -o -user nobody  -o  -user root  -o -user mysql \) -print -exec chown ${CPANELUSER} {} \;

  echo "***  Done..   ***"

fi

fi
