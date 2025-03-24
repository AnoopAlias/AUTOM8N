#!/usr/bin/env bash

CPANELUSER="${1}"
HOMEDIR=$( getent passwd "${CPANELUSER}" | cut -d: -f6 )
if [ -d ${HOMEDIR} ]; then
  echo "*** Fixing ownership and group of account ${CPANELUSER} ***"
  
  find /home/${user}/ -not \( -group ${user} -o -group nobody -o -group mail  \) -print -exec chgrp ${user} {} \;
  find /home/${user}/ -not -user ${user} -print -exec chown chgrp ${user} {} \;

  echo "***  Done..   ***"

fi
