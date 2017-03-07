#!/bin/bash

# Meant to be run from a cronjob to shutdown unused phpfpm processes
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1);do nice --adjustment=15 /opt/nDeploy/scripts/phpfpm_ghost_hunter.py $CPANELUSER;done
