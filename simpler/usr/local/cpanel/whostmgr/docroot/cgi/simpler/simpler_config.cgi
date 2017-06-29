#!/usr/bin/env python


import cgitb
import cgi
import os
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
print('<h4><span class="label label-primary">SimpleR</span></h4>')
print('<h6><span class="label label-default">Simple Resouce controller</span></h6>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="simpler.cgi"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li class="active">Modify Resource</li>')
print('</ol>')
mem = psutil.virtual_memory()
# mycpucount = psutil.cpu_count()
good_mem_limit = str((mem.total / (1024 * 1024)) * 0.8)
if form.getvalue('mode'):
    if form.getvalue('mode') == "user":
        if form.getvalue('reseller'):
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Modify resellers resource</span></h3></div>')
            print('<div class="panel-body">')

            thereseller = form.getvalue('reseller')
            ownerslice = "/etc/systemd/system/"+thereseller+".slice"
            config = ConfigParser()
            config.optionxform = str
            config.read(ownerslice)
            CPUWeight = config.get('Slice', 'CPUShares')
            MemoryHigh = config.get('Slice', 'MemoryLimit')
            IOWeight = config.get('Slice', 'BlockIOWeight')

            print(('<div class="panel-heading"><h3 class="panel-title">Current Resource Settings: '+thereseller+'</h3></div>'))
            print(('<div class="panel-body">'))
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>CPUWeight</strong></div></div>')
            print(('<div class="col-sm-6"><div class="label label-warning">'+CPUWeight+'</div></div>'))
            print('</div>')
            print('</li>')

            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>MemoryHigh</strong></div></div>')
            print(('<div class="col-sm-6"><div class="label label-warning">'+MemoryHigh+'</div></div>'))
            print('</div>')
            print('</li>')

            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>IOWeight</strong></div></div>')
            print(('<div class="col-sm-6"><div class="label label-warning">'+IOWeight+'</div></div>'))
            print('</div>')
            print('</li>')

            print('</div>')

            print(('<div class="panel-heading"><h3 class="panel-title">New Resource Settings: '+thereseller+'</h3></div>'))
            print(('<div class="panel-body">'))
            print('<form id="config" class="form-inline config-save" action="simpler_save.cgi" method="post">')
            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>CPUWeight</strong></div></div>')
            print(('<div class="col-sm-6">'))
            print('<input class="form-control" placeholder="1024" type="text" name="cpuweight">')
            print(('</div>'))
            print('</div>')
            print('</li>')

            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>MemoryHigh</strong></div></div>')
            print(('<div class="col-sm-6">'))
            print('<input class="form-control" placeholder="4G" type="text" name="memoryhigh">')
            print(('</div>'))
            print('</div>')
            print('</li>')

            print('<li class="list-group-item">')
            print('<div class="row">')
            print('<div class="col-sm-6"><div class="label label-default"><strong>IOWeight</strong></div></div>')
            print(('<div class="col-sm-6">'))
            print('<input class="form-control" placeholder="10-1000" type="text" name="ioweight">')
            print(('</div>'))
            print('</div>')
            print('</li>')

            print('</div>')

            print(('<input style="display:none" name="mode" value="user">'))
            print(('<input style="display:none" name="reseller" value="'+thereseller+'">'))
            print('<input class="btn btn-primary" type="submit" value="Submit">')

            print('</form>')
            print('</div>')
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>'+good_mem_limit+'M (80% of your total memory) is a good upper limit</div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
        else:
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
    elif form.getvalue('mode') == "service":
        if form.getvalue('service'):
            myservice = form.getvalue('service')
            print('<div class="panel panel-default">')
            print('<div class="panel-heading"><h3 class="panel-title"><span class="label label-default">Modify service resource</span></h3></div>')
            print('<div class="panel-body">')
            if os.path.isfile('/etc/systemd/system/' + myservice + '.service.d/limits.conf'):
                limitsconf = '/etc/systemd/system/' + myservice + '.service.d/limits.conf'
                config = ConfigParser()
                config.optionxform = str
                config.read(limitsconf)
                CPUWeight = config.get('Service', 'CPUShares')
                MemoryHigh = config.get('Service', 'MemoryLimit')
                IOWeight = config.get('Service', 'BlockIOWeight')

                print(('<div class="panel-heading"><h3 class="panel-title">Current Resource Settings: ' + myservice + '</h3></div>'))
                print(('<div class="panel-body">'))

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>CPUWeight</strong></div></div>')
                print(('<div class="col-sm-6"><div class="label label-warning">'+CPUWeight+'</div></div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>MemoryHigh</strong></div></div>')
                print(('<div class="col-sm-6"><div class="label label-warning">'+MemoryHigh+'</div></div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>IOWeight</strong></div></div>')
                print(('<div class="col-sm-6"><div class="label label-warning">'+IOWeight+'</div></div>'))
                print('</div>')
                print('</li>')

                print('</div>')

                print(('<div class="panel-heading"><h3 class="panel-title">New Resource Settings: ' + myservice + '</h3></div>'))
                print(('<div class="panel-body">'))
                print('<form id="config" class="form-inline config-save" action="simpler_save.cgi" method="post">')
                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>CPUWeight</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="1024" type="text" name="cpuweight">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>MemoryHigh</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="4G" type="text" name="memoryhigh">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>IOWeight</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="10-1000" type="text" name="ioweight">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('</div>')

                print(('<input style="display:none" name="service" value="'+myservice+'">'))
                print(('<input style="display:none" name="mode" value="service">'))
                print('<input class="btn btn-primary" type="submit" value="Submit">')

                print('</form>')
                print('</div>')
            else:
                print(('<div class="panel-heading"><h3 class="panel-title">Current Resource Settings: '+myservice+'</h3></div>'))
                print(('<div class="panel-body">'))

                print('<li class="list-group-item">')
                print('<div class="row">')
                print(('<div class="label label-warning">No Limit</div>'))
                print('</div>')
                print('</li>')
                print('</div>')

                print(('<div class="panel-heading"><h3 class="panel-title">New Resource Settings: '+myservice+'</h3></div>'))
                print(('<div class="panel-body">'))
                print('<form id="config" class="form-inline config-save" action="simpler_save.cgi" method="post">')
                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>CPUWeight</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="1024" type="text" name="cpuweight">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>MemoryHigh</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="4G" type="text" name="memoryhigh">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('<li class="list-group-item">')
                print('<div class="row">')
                print('<div class="col-sm-6"><div class="label label-default"><strong>IOWeight</strong></div></div>')
                print(('<div class="col-sm-6">'))
                print('<input class="form-control" placeholder="10-1000" type="text" name="ioweight">')
                print(('</div>'))
                print('</div>')
                print('</li>')

                print('</div>')

                print(('<input style="display:none" name="service" value="'+myservice+'">'))
                print(('<input style="display:none" name="mode" value="service">'))
                print('<input class="btn btn-primary" type="submit" value="Submit">')

                print('</form>')
                print('</div>')
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>'+good_mem_limit+'M (80% of your total memory) is a good upper limit</div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
        else:
            print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
            print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
    else:
        print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
        print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
else:
    print('<div class="alert alert-info"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden </div>')
    print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
