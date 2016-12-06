#!/bin/bash

# Meant to be run from a cronjob to shutdown unused hhvm processes
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);do nice --adjustment=15 /opt/nDeploy/scripts/hhvm_ghost_hunter.py $CPANELUSER;done
