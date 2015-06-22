#!/bin/sh

whois -h whois.radb.net -- '-i origin AS32934' | grep route: | awk '{print $2}' | sort | uniq > facebook_ips.txt