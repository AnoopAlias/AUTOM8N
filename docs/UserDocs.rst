XtendWeb User docs
=======================

Setup URL Redirects
-----------------------
.. note:: URL redirects setup from cPanel is done via .htaccess file and will work only in PROXY mode . For native nginx (nginx+php-fpm etc),you will need to setup the redirects in XtendWeb plugin
          All rdirect types can be easily setup from XtendWeb plugin


.. youtube:: https://www.youtube.com/watch?v=jVwvUBnUXUQ


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

Custom nginx configuration
--------------------------------

To enable custom configuration ,please upload configuration to be placed in the server{} section of your nginx configuration
in the application's root folder (eg; /home/user/public_html/nginx.conf)

Once done. You can activate the config from

cPanel >> XtendWeb >> Server Settings >> user_config

set to [enabled]

What pagespeed filters are active?
-------------------------------------------

You can view the active filters using
::

  curl -H "PageSpeedFilters: +debug" https://example.com
  # example.com must be substituted with your domain name
