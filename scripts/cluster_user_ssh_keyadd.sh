#!/usr/bin/env bash

if [ -d ~/.ssh ]
then
  if [ -f ~/.ssh/clusterkey ]
  then
    # Ensure key is in authorized_keys
    THECLUSTERKEY=$(cat ~/.ssh/clusterkey.pub)
    grep -w "${THECLUSTERKEY}" ~/.ssh/authorized_keys > /dev/null 2>&1 || cat ~/.ssh/clusterkey.pub >> ~/.ssh/authorized_keys
    chmod 400 ~/.ssh/authorized_keys
    echo "PasswordAuthentication no" > ~/.ssh/config
    chmod 400 ~/.ssh/config
  else
    ssh-keygen -b 2048 -t rsa -f ~/.ssh/clusterkey -q -N ""
    # Ensure key is in authorized_keys
    THECLUSTERKEY=$(cat ~/.ssh/clusterkey.pub)
    grep -w "${THECLUSTERKEY}" ~/.ssh/authorized_keys > /dev/null 2>&1 || cat ~/.ssh/clusterkey.pub >> ~/.ssh/authorized_keys
    chmod 400 ~/.ssh/authorized_keys
    echo "PasswordAuthentication no" > ~/.ssh/config
    chmod 400 ~/.ssh/config
  fi
else
  mdir ~/.ssh
  chmod 400 ~/.ssh
  ssh-keygen -b 2048 -t rsa -f ~/.ssh/clusterkey -q -N ""
  # Ensure key is in authorized_keys
  THECLUSTERKEY=$(cat ~/.ssh/clusterkey.pub)
  grep -w "${THECLUSTERKEY}" ~/.ssh/authorized_keys > /dev/null 2>&1 || cat ~/.ssh/clusterkey.pub >> ~/.ssh/authorized_keys
  chmod 400 ~/.ssh/authorized_keys
  echo "PasswordAuthentication no" > ~/.ssh/config
  chmod 400 ~/.ssh/config
fi
