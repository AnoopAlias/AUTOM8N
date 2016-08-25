brotli_compression
===================

Brotli is a relatively new compression format that provides 20% more compression over deflate

Ref: http://google-opensource.blogspot.in/2015/09/introducing-brotli-new-compression.html

nginx-nDeploy comes compiled with brotli support ;but it is not enabled by default as the compression is
a bit more CPU intensive than gzip. If your clients want more faster pageload and you have CPU resources to spare,
brotli can be enabled using the following command

``echo "include /etc/nginx/conf.d/brotli.conf;" >> /etc/nginx/conf.d/custom_include.conf``

All newer Versions of Chrome,FireFox,Opera support brotli and prefers brotli over other compression if enabled

.. disqus::
