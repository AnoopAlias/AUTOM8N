XtendWeb User docs
=======================

Setup URL Redirects
-----------------------
.. note:: URL redirects setup from cPanel is done via .htaccess file and will work only in PROXY mode . For native nginx (nginx+php-fpm etc),you will need to setup the redirects in XtendWeb plugin
          All rdirect types can be easily setup from XtendWeb plugin


.. youtube:: https://www.youtube.com/watch?v=jVwvUBnUXUQ

1. domain.com to www.domain.com - Select domain in XtendWeb » Server Settings » www redirect

2. http://domain.com to https://domain.com - Select domain in XtendWeb » Server Settings » redirect_to_ssl

.. tip:: if you enable hsts in server settings, web browsers would prefer https:// over http://

3. http://my-alias-domain.com to http://domain.com - Select domain in XtendWeb » Server Settings » redirect_aliases

4. http://domain.com to http://external-domain.com - Select domain in XtendWeb » Server Settings
::

  1. URL Redirect  - Select Permanent redirect
  2. append $request_uri to redirecturl   # eg:  http://domain.com/?q=test would be redirected to http://external-domain.com/?q=test
  3. Redirect to URL  - Enter target URL here # eg: http://external-domain.com

5. http://domain.com/blog to http://external-domain.com - Select domain in XtendWeb » Subdir Apps
::

  Enter /blog in "Add new subdirectory apps"
  Select Any Backend , Version and Application template # This will be replaced by the redirect shortly so you can select any
  Save

  Click on "Subdir Apps" Again and Click on "Edit" beside the subdir you already added
  In Application Settings

  1. URL Redirect  - Select Permanent redirect
  2. append $request_uri to redirecturl  [ Set enabled/disabled ]
  3. Redirect to URL  - Enter target URL here # eg: http://external-domain.com or http://domain.com/mynewblog

.. tip:: To redirect domain.com/blog to domain.com/newblog follow the same procedure as step 5 above and enter
         domain.com/newblog as the "Redirect to URL"

Enable Directory listing
---------------------------

XtendWeb » Server Settings » autoindex [ enabled ]


Content Optimization
--------------------------

Following optimizes your html pages

1. pagespeed - provides html pages optimised for speed . it rewrites and modifies resources onyour webpage

.. note:: "PassThrough" pagespeed level may sometime break page rendering . Select CoreFilters for a less drastic optimization

2. brotli and gzip  -  Both brotli and gzip reduce content size ,brotli gives 20% more reduction but works over https:// only

Security Headers
------------------------
clickjacking_protect - Disallow Iframe to be loaded in your website from external domains . Disable this feature if you have external iframe

disable_contenttype_sniffing - Read https://www.keycdn.com/support/what-is-mime-sniffing/ - Keeping this option [ enabled ] is good

xss_filter -Read https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-XSS-Protection - Keeping this option [ enabled ] is good
