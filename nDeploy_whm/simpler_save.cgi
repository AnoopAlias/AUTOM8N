#!/usr/bin/env python


import cgitb
import subprocess
import os
import cgi
import shutil
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
print('<title>SimpleR Resource control</title>')
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
print('<a href="simpler.cgi" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>Simple Resource Controller</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="simpler.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Save Resource</li>')
print('</ol>')
if form.getvalue('mode'):
    if form.getvalue('mode') == 'user':
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
            print(('<div class="panel-heading"><h3 class="panel-title">Reseller: <strong>'+thereseller+'</strong></h3></div>'))
            print('<div class="panel-body">')
            with open(ownerslice, 'w') as configfile:
                config.write(configfile)
            subprocess.call(['systemctl', 'daemon-reload'])
            subprocess.Popen('/opt/nDeploy/scripts/attempt_autofix.sh', shell=True)
            print('<div class="icon-box">')
            print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Resource settings saved')
            print('</div>')
            print('</div>')
            print('</div>')

            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
            print('</div>')
        else:
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>Forbidden</div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
    elif form.getvalue('mode') == 'service':
        if form.getvalue('service') and form.getvalue('cpuweight') and form.getvalue('memoryhigh') and form.getvalue('ioweight'):
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Save service resource</span></h3></div>')
            print('<div class="panel-body">')

            myservice = form.getvalue('service')
            limitsconf = '/etc/systemd/system/' + myservice + '.service.d/limits.conf'
            if not os.path.isdir('/etc/systemd/system/'+myservice+'.service.d'):
                os.mkdir('/etc/systemd/system/'+myservice+'.service.d', 0o755)
            if not os.path.isfile(limitsconf):
                shutil.copyfile(xtendweb_installation_path+'/conf/simpler_service_resources.j2', limitsconf)
            config = ConfigParser()
            config.optionxform = str
            config.read(limitsconf)
            config.set('Service', 'CPUShares', form.getvalue('cpuweight'))
            config.set('Service', 'MemoryLimit', form.getvalue('memoryhigh'))
            config.set('Service', 'BlockIOWeight', form.getvalue('ioweight'))
            print(('<div class="panel-heading"><h3 class="panel-title">Service: <strong>'+myservice+'</strong></h3></div>'))
            print('<div class="panel-body">')
            with open(limitsconf, 'w') as configfile:
                config.write(configfile)
            subprocess.call(['systemctl', 'daemon-reload'])
            subprocess.Popen(['systemctl', 'restart', myservice])
            print('<div class="icon-box">')
            print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Resource settings saved')
            print('</div>')
            print('</div>')
            print('</div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
            print('</div>')
        else:
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>Forbidden</div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
else:
    print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span>Forbidden</div>')
    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
