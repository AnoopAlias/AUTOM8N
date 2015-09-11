#!/bin/bash

ulimit -n 10000
/etc/init.d/nginx configtest && /etc/init.d/nginx reload