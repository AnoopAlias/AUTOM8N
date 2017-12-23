#!/usr/bin/env python


import cgitb
import subprocess
import os
import cgi
import shutil
import psutil
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
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')  # marker1
print('<div class="row">')  # marker2
print('<div class="col-md-6 col-md-offset-3">')  # marker3
print('<div class="logo">')
print('<a href="xtendweb.cgi" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Server Config</li>')
print('</ol>')

if form.getvalue('mode') and form.getvalue('unit') and form.getvalue('cpu') and form.getvalue('memory') and form.getvalue('blockio'):
  if form.getvalue('mode') == 'service':
    myservice = form.getvalue('unit')+".service"
  elif form.getvalue('mode') == 'user':
    myservice = form.getvalue('unit')+".slice"
  print('<div class="panel panel-default">')
  print(('<div class="panel-heading"><h3 class="panel-title">Save Resource limit:'+myservice+'</h3></div>'))
  print('<div class="panel-body">')  # marker6
  if form.getvalue('cpu') == '50':
   subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=512', shell=True)
  elif form.getvalue('cpu') == '75':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=768', shell=True)
  elif form.getvalue('cpu') == '100':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUShares=1024', shell=True)
  if form.getvalue('blockio') == '50':
   subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=500', shell=True)
  elif form.getvalue('blockio') == '75':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=750', shell=True)
  elif form.getvalue('blockio') == '100':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOWeight=1000', shell=True)
  mymem = psutil.virtual_memory().total
  mem_threequarter = float(mymem) * 0.75
  mem_half = float(mymem) / 2.0
  if form.getvalue('memory') == '50':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+int(mem_half), shell=True)
  elif form.getvalue('memory') == '75':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+int(mem_threequarter), shell=True)
  elif form.getvalue('memory') == '100':
    subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryLimit='+mymem, shell=True)
  subprocess.call('/usr/bin/systemctl set-property '+myservice+' CPUAccounting=yes', shell=True)
  subprocess.call('/usr/bin/systemctl set-property '+myservice+' BlockIOAccounting=yes', shell=True)
  subprocess.call('/usr/bin/systemctl set-property '+myservice+' MemoryAccounting=yes', shell=True)
  subprocess.call('/usr/bin/systemctl daemon-reload', shell=True)
  print('<div class="icon-box">')
  print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Resource Settings updated')
  print('</div>')

  print('</div>') # markera2
  print('</div>') # markera1

else:
  print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
