Full Page cache
=======================

XtendWeb support full page caching for popular CMS Wordpress and Drupal.

A dynamic website is one where content is generated dynamically by an application server .This makes a dynamic website hugely dependant on MySQL and PHP (assuming LAMP stack)
for each and every page request. One of the mechanism to make the dependancy less is caching. There are various levels at which the cache can be configured.

1. WebServer level - Proxy cache, FastCGI cache and Subrequest cache are 3 common example for this
   The webserver level caches are mostly fastest because it just need the webserver to fullfill the page request.
   Note that dynamic application sets various cookies and headers so that browsers,proxies etc do not cache the content.So special config is needed in
   webserver to ignore these cookies and headers and cache content that are cacheable

2. Application level caches - These caches are setup at application level and will require support from both application(like an extra module) and the web server to cache content
   These are often less speedier than webserver level cache as the application server is also involved. Common Examples are W3TC and WPSuperCache in wordpress. Some appliation caches do not
   need any special changes to webserver config and works purely by modifying application code.


.. note:: What is good for cache? - A blog or e-newspaper or mostly static content served by a dynamic app like wordpress/drupal.
         What is not good to be cached? - An ecommerce shopping cart , personal non static content etc


Full page cache to redis
--------------------------

XtendWeb support very high performing full page cache to redis for wordpress and Drupal. This use the https://github.com/openresty/srcache-nginx-module to cache the fully rendered page in redis.

To enable the templates run
::

  /opt/nDeploy/scripts/setup_additional_templates.sh

The above step will setup 3 additional templates

1. Wordpress+Redis+nginx-helper  - You will need to install https://wordpress.org/plugins/nginx-helper/ plugin in wordpress to invalidate cache on changes to content.There is no prefix used so leave
   the prefix field blank in plugin setup.There is no seperate cache for mobile and desktop devices in this template

2. Wordpress+Redis  - No additional module is required for this cache to work. Every page is cached for 10 miutes after which the cached data gets invalidated. Seperate cache exist for mobile and desktop
   versions of the website.

3. Drupal+Redis  - No additional module is required for this cache to work. Every page is cached for 10 miutes after which the cached data gets invalidated. Seperate cache exist for mobile and desktop
   versions of the website.

The cache logic ignore all application level cookies and urls except

For Wordpress
::


    map $request_method $requestnocache {
        default "";
        POST    1;
    }


    map $http_cookie $wpcookienocache {
            default                     "";
            SESS                        1;
            PHPSESSID                   1;
            ~*wordpress_[a-f0-9]+       1;
            comment_author              1;
            wp-postpass                 1;
            wordpress_no_cache          1;
            woocommerce_items_in_cart   1;
            wp_woocommerce.*            1;
            woocommerce_cart.*          1;
            resetpass                   1;
            wordpress_logged_in         1;
            wordpress_sec*              1;
            wp-settings*                1;
        }


    map $request_uri $wpurinocache {
            default                                      "";
            ~*^\/wp-admin.*                              1;
            ~*^\/wp-[a-zA-Z0-9-]+\.php$                  1;
            ~*^\/feed\/.*                                1;
            ~*^\/administrator\/.*                       1;
            ~*^\/xmlrpc.php$                             1;
            ~*^\/index.php$                              1;
            ~*^\/wp-links-opml.php$                      1;
            ~*^\/wp-locations.php$                       1;
            ~*^\/sitemap(_index)?.xml                    1;
            ~*^\/[a-z0-9_-]+-sitemap([0-9]+)?.xml        1;
            ~*^\/cart.*                                  1;
            ~*^\/my-account\/.*                          1;
            ~*^\/wp-api\/.*                              1;
            ~*^\/resetpass\/.*                           1;
    }



For Drupal
::

    map $request_method $requestnocache {
        default "";
        POST    1;
    }

    map $http_cookie $drupalcookienocache {
            default                     "";
            ~*SESS                        1;
        }

    map $request_uri $drupalurinocache {
            default                 "";
            ~*\/status\.php$         1;
            ~*\/update\.php$         1;
            ~*\/admin$              1;
            ~*\/admin\/.*$          1;
            ~*\/user$               1;
            ~*\/user\/.*            1;
            ~*\/flag\/.*            1;
            ~*.*\/ajax\/.*          1;
            ~*.*\/ahah\/.*          1;
            ~*\/admin\/content\/backup_migrate\/export  1;
      }


Note that the above list of cookies and URL's can be extended by the admnistrator in /etc/nginx/conf.d/maps.conf
