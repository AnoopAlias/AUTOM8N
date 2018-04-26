#!/usr/bin/env python

import httplib
import re
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
server = "master.example.com"


def is_page_available(host, path="/nginx_status"):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        False.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        if re.match("^[23]\d\d$", str(conn.getresponse().status)):
            return True
    except StandardError:
        return None


if __name__ == "__main__":
    if is_page_available(server, "/nginx_status"):
        subprocess.Popen(['/usr/bin/systemctl', 'stop', 'nginx.service'])
    else:
        subprocess.Popen(['/usr/bin/systemctl', 'start', 'nginx.service'])
