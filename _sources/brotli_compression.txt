brotli_compression
===================

Brotli is a relatively new compression format that provides 20% more compression over deflate

Ref: http://google-opensource.blogspot.in/2015/09/introducing-brotli-new-compression.html

.. tip:: Brotli on the fly compression is CPU intensive

To enable brotli do
::

  yum --enablerepo=ndeploy install nginx-nDeploy-module-brotli

Once the module is installed brotli can be turned on/off from the plugin user interface in cPanel

You can check if brotli is enabled using : https://tools.keycdn.com/brotli-test

All newer Versions of Chrome,FireFox,Opera support brotli and prefers brotli over other compression if enabled

.. disqus::
