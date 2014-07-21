xstack
======

cpanel nginx stack plugin

How it works?
======
Cpanel stores apache config data in yaml at /var/cpanel/userdata . xstack intend to provide users with another config data store at /opt/xstack/userdata which they can populate using a UI in their cpanel and the xstack backend will be able to generate nginx configuration from the above two config data files at any point given the cpanel username as argument .

Account profile
======
This data is stored in /opt/xstack/useradata in yaml and states what is the profile of nginx configuration that a user want for the account .For example user can say "I want an nginx profile for Magento" which will tell the nginx config generator what configuration template must be used for the account and thereby reducing end user effort in configuring his nginx vhost 

Programming language
======
The backend is scripted in Python . The User Interface is scripted in PHP
