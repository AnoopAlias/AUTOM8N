brotli_compression
===================

Brotli is a relatively new compression format that provides `~20-26% higher compression over deflate <http://google-opensource.blogspot.in/2015/09/introducing-brotli-new-compression.html>`_.

nginx-nDeploy comes compiled with Brotli support; but it is not enabled by default as the compression is
a bit more CPU intensive than gzip. If your clients want more faster pageload and you have CPU resources to spare,
Brotli can be enabled using the following command:

``echo "include /etc/nginx/conf.d/brotli.conf;" >> /etc/nginx/conf.d/custom_include.conf``

You can check if Brotli is enabled using the `KeyCDN Brotli Test <https://tools.keycdn.com/brotli-test>`_.

All newer versions of Chrome, Firefox, Opera support Brotli and prefer Brotli over other compression if enabled. Check for Brotli support in browser versions at `caniuse <http://caniuse.com/#search=brotli>`_.

.. disqus::
