Application templates
=========================

.. caution:: Do NOT include location like the follwing in a template
::
location ~* \.(?:jpg|jpeg|gif|png|ico|cur|gz|svg|svgz|mp4|ogg|ogv|webm|htc)$ {}

nginx config file is not Apache httpd compatible. Most web applications ship requirements like rewrite rules
in an htaccess file hoping the app will be run on Apache httpd server .

Application template are XtendWeb's answer to htaccess config in nginx world.

A bare minimum PHP webapp template is
::


  location / {
  try_files $uri $uri/ /index.php;
  }

  #Required for php ping/pong monitoing to work
  location ~ ^/pingphpfpm$ {
  include /etc/nginx/fastcgi_params*;
  fastcgi_pass unix:{{ SOCKETFILE }};
  }

  location ~ \.php$ {
  try_files $uri =404;
  fastcgi_pass unix:{{ SOCKETFILE }};
  fastcgi_index index.php;
  include /etc/nginx/fastcgi_params*;
  }

  #Required to redirect /cpanel /whm etc
  include /etc/nginx/conf.d/cpanel_services.conf;


Additionally if you wish to support some optional functionality like NAXSI,Apps in SubFolder etc a corresponding Jinja2 is required

For NAXSI you need to add the following inside location{} blocks
::

  # Include NAXSI settings
  {% if NAXSI == 'enabled' %}
  {% if NAXSIMODE == 'learn' %}
  include /etc/nginx/conf.d/naxsi_learn.rules;
  {% if NAXSI_WHITELIST == 'wordpress' %}
  include /etc/nginx/naxsi.d/wordpress.rules;
  {% endif %}
  {% if NAXSI_WHITELIST == 'drupal' %}
  include /etc/nginx/naxsi.d/drupal.rules;
  {% endif %}
  {% elif NAXSIMODE == 'active' %}
  include /etc/nginx/conf.d/naxsi_active.rules;
  {% if NAXSI_WHITELIST == 'wordpress' %}
  include /etc/nginx/naxsi.d/wordpress.rules;
  {% endif %}
  {% if NAXSI_WHITELIST == 'drupal' %}
  include /etc/nginx/naxsi.d/drupal.rules;
  {% endif %}
  {% endif %}
  include /etc/nginx/sites-enabled/{{ CONFIGDOMAINNAME }}_{{ SUBDIRAPPS[SUBDIR] }}.naxsi.wl*;
  {% endif %}
  # End Include NAXSI settings

For a subdirectory template; you need to include the following for some settings to work
::

  {% if AUTH_BASIC == 'enabled' %}
  auth_basic "Restricted Content";
  auth_basic_user_file {{ HOMEDIR }}/.htpasswds{{ DIFFDIR }}/{{ SUBDIR }}/passwd;
  {% endif %}

  {% if REDIRECTSTATUS != 'none' and REDIRECT_URL != 'none'  %}
  return {{REDIRECTSTATUS}} {{REDIRECT_URL}}{% if APPEND_REQUESTURI == 'enabled' %}$request_uri{% endif %};
  {% else %}

  {% if SET_EXPIRE_STATIC == 'enabled' %}
  include /etc/nginx/conf.d/files_with_expire.conf;
  {% endif %}


Thats it! .
