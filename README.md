nDeploy
======

cpanel nginx plugin that lets users deploy multiple scripts .The current list of backends supported are 

PHP - via PHP-FPM ( FastCGI protocol)
Ruby - Rails application via Phusion Passenger
Python - WSGI compliant apps via Phusion Passenger
NodeJS - via Phusion Passenger
ColdFusion - Generic Proxy to Railo/OpenBD 

All script engines will be deployed using a popular multi version manager of the same.
PHP - phpbrew
RUBY - rvm
Python - pythonz
NodeJS - nvm

This helps the server admins to provide virtually unlimited versions of the popular scripting engines to end users.


Application Architecture:
======

Backend script - which generates nginx configuration and spawns backend( if required ) running under root privilege .The script gets triggered by file system events generated when a config change is commited by cpanel daemon or via the nDeploy user interface . The script is kept simple with ~300 lines of python code to improve security and enhance simplicity

Plugin script - Complies to cpanel plugin architecture and presents a user interface . Written in PHP mainly due to the easiness to do so.

Because we mostly depend on file system events ; we are mostly unaffected by changes in cpanel hooks and API's.


How can you contribute?
======
The easiest way to contribute is to submit nginx config templates ( profiles as we call it) for various applications (mostly PHP) 
A sample profile (configuration for nginx) for deploying a wordpress application can be found at conf/1001.tmpl

You can also review the main scripts and submit enhancements .

