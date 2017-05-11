#!/usr/bin/env python


import os
import cgitb
import subprocess
import jinja2
import codecs
import cgi
try:
    import simplejson as json
except ImportError:
    import json
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser



__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


xtendweb_installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()
form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>SimpleR Reseller Resource control</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<h4><span class="label label-primary">Simple</span><span class="label label-default">R</span></h4>')
print('<h6><span class="label label-default">Reseller Resouce controller</span></h6>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="simpler.cgi"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li class="active">Save Reseller Resource</li>')
print('</ol>')
if form.getvalue('reseller') and form.getvalue('cpuweight') and form.getvalue('memoryhigh') and form.getvalue('ioweight'):
    print('<div class="panel panel-default">')
    print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Save reseller resource</span></h3></div>')
    print('<div class="panel-body">')

    thereseller = form.getvalue('reseller')
    ownerslice = "/etc/systemd/system/"+thereseller+".slice"
    config = ConfigParser()
    config.optionxform = str
    config.read(ownerslice)
    config.set('Slice', 'CPUShares', form.getvalue('cpuweight'))
    config.set('Slice', 'MemoryLimit', form.getvalue('memoryhigh'))
    config.set('Slice', 'BlockIOWeight', form.getvalue('ioweight'))
    with open(ownerslice, 'w') as configfile:
      config.write(configfile)
    print(('<div class="panel-heading"><h3 class="panel-title">Reseller: <strong>'+thereseller+'</strong></h3></div>'))
    print('<div class="panel-body">')
    with open(ownerslice, 'w') as configfile:
      config.write(configfile)
    subprocess.call(['systemctl', 'daemon-reload'], shell=True)
    print('<div class="icon-box">')
    print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Resource settings saved')
    print('</div>')

    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://xtendweb.gnusys.net/docs/user_docs.html">XtendWeb Docs</a></small></div>')
    print('</div>')
else:
    print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>Forbidden</div>')
    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://xtendweb.gnusys.net/docs/user_docs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
