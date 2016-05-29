#!/bin/bash
#Author : Anoop P Alias

postconf -e "smtpd_recipient_restrictions = permit_sasl_authenticated, permit_mynetworks, reject_unauth_destination"
postconf -e "relay_recipient_maps ="
postconf -e "relay_domains = hash:/etc/postfix/relaydomains"
postconf -e "inet_interfaces = all"
