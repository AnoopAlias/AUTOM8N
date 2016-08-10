LetsEncrypt with nDeploy
=========================

.. tip:: *Note that this feature will be depricated in future versions of nDeploy.*


1. You need to install the certbot official client from https://certbot.eff.org/

2. create the file /opt/nDeploy/conf/letsencrypt.yaml which should contain
::

  letsencrypt: "path to letsencrypt or certbot binary in quotes"
  email: "admin email address in quotes"

For example
::

  root@cpanel [~]# cat /opt/nDeploy/conf/letsencrypt.yaml
  letsencrypt: "/usr/bin/certbot"
  email: "cert_renewels@sysally.net"

3. Once step 2 is complete. the nDeploy GUI will show up LetsEncrypt cert setup
Note that the GUI is running the following command
::

  /usr/bin/certbot --email  cert_renewels@sysally.net --text --renew-by-default --agree-tos --server https://acme-v01.api.letsencrypt.org/directory certonly -a webroot --webroot-path /home/user/public_html/ -d cpanel_main_domain -d cpanel_alias1 -d cpanel_alias2

So the command will fail unless the main_domain along with all aliases resolve to the server

4. Check the auto-renew setting
::

  /usr/bin/certbot renew


Once you find it error free ;add the command to roots cron and run it once daily

5. If you are proxying to cPanel http server note that the SSL vhost is only present in nginX and not apache in nDeploys LetsEncrypt implementation.
So You will need to use PROXY >> apache >> Proxy to cPanel httpd rather than PROXY >> apache_SSL >> Proxy to cPanel httpd(SSL)

6. For generating the Cert
::

  Login to cPanel and select the nginX plugin

  Select domain.com >> CONFIGURE >> AUTO >> SUBMIT

  BACKEND : PROXY
  Backend Type : You can select anything here
  Select a configuration template: LetsEncrypt

  and SAVE

  This will make your site config suitable for ACME challenge response (it will make the http://domain.com inaccessible for security reasons)

  Once this is done reload the config generator by clicking on the nginX icon

  domain.com >> LETSENCRYPT CERT INSTALL >> ENABLE >> SUBMIT

  The cert will now get setup . You can revert the config template for non-SSL domain to the original setting now . You will also find that that there is a domain.com_SSL vhost to configure now .

.. disqus::
