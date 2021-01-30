#!/usr/bin/env python3


import configparser


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


config = configparser.ConfigParser()
config.read('/root/.my.cnf')
mypass = config.get('client', 'password')
if mypass.startswith('"') and mypass.endswith('"'):
    temppass = mypass.lstrip('"').rstrip('"')
    config.set('client', 'password', "'"+temppass+"'")
    with open('/root/.my.cnf', 'w') as configfile:
        config.write(configfile)
else:
    if not mypass.startswith("'") and mypass.endswith("'"):
        config.set('client', 'password', "'"+mypass+"'")
        with open('/root/.my.cnf', 'w') as configfile:
            config.write(configfile)
