#!/usr/bin/env python


import cgitb
import cgi
import os
import psutil
import subprocess
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

if form.getvalue('mode') and form.getvalue('unit'):
  if form.getvalue('mode') == 'service':
    myservice = form.getvalue('unit')+".service"
    print('<div class="panel panel-default">')
    print(('<div class="panel-heading"><h3 class="panel-title">Current Resource usage:</h3></div>'))
    print('<div class="panel-body">')  # marker6
    print('<ul class="list-group">')
    print(('<div class="alert alert-info alert-top">'))
    mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
    mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
    myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
    if int(myio) == 18446744073709551615:
      print('BlockIOWeight=nolimit')
    else:
      print('BlockIOWeight='+myio)
    print('<br>')
    if int(mycpu) == 18446744073709551615:
      print('CPUShares=nolimit')
    else:
      print('CPUShares='+mycpu)
    print('<br>')
    if int(mymem) == 18446744073709551615:
      print('MemoryLimit=nolimit')
    else:
      mymem_inmb=float(mymem) / ( 1024.0 * 1024.0 )
      print('CPUShares='+str(mymem_inmb)+'Mb')
    print('<br>')
    print(('</div>'))
    print('</ul>')
    print('</div>')  # marker6
    print('</div>')
  elif form.getvalue('mode') == 'user':
    myservice = form.getvalue('unit')+".slice"
    print('<div class="panel panel-default">')
    print(('<div class="panel-heading"><h3 class="panel-title">Current Resource usage:</h3></div>'))
    print('<div class="panel-body">')  # marker6
    print('<ul class="list-group">')
    print(('<div class="alert alert-info alert-top">'))
    mymem = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  MemoryLimit', shell=True).split('=')[1]
    mycpu = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  CPUShares', shell=True).split('=')[1]
    myio = subprocess.check_output('/usr/bin/systemctl show '+myservice+' -p  BlockIOWeight', shell=True).split('=')[1]
    if int(myio) == 18446744073709551615:
      print('BlockIOWeight=nolimit')
    else:
      print('BlockIOWeight='+myio)
    print('<br>')
    if int(mycpu) == 18446744073709551615:
      print('CPUShares=nolimit')
    else:
      print('CPUShares='+mycpu)
    print('<br>')
    if int(mymem) == 18446744073709551615:
      print('MemoryLimit=nolimit')
    else:
      mymem_inmb=float(mymem) / ( 1024.0 * 1024.0 )
      print('CPUShares='+str(mymem_inmb)+'Mb')
    print('<br>')
    print(('</div>'))
    print('</ul>')
    print('</div>')  # marker6
    print('</div>')
else:
  print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')

print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
