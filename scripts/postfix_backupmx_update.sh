#!/bin/bash
#Author : Anoop P Alias
#csync2 action script to configure postfix relaydomains in cPanel
sed 's/$/ OK/' /etc/localdomains > /etc/postfix/relaydomains
chmod 644 /etc/postfix/relaydomains
postmap /etc/postfix/relaydomains
postfix reload
