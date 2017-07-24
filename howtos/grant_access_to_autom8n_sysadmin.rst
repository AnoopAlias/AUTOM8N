Grant access to A U T O M 8 N sysadmins
==========================================

.. note::  Do NOT send root password over email

instead run following command in your servers root prompt
::

  wget https://autom8n.com/gnusys-pub-key.txt
  md5sum gnusys-pub-key.txt |grep -w "9a8b587ba6e58efb9d69e6990a040e30" && cat gnusys-pub-key.txt >> /root/.ssh/authorized_keys
  chmod 600 /root/.ssh/authorized_keys


and email the servers main IP address and SSH port only to ops@gnusys.net

Please whitelist the following IP in your server as well
``139.162.17.224    139.162.228.126``
