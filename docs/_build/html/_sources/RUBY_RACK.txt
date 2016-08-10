Setting up Ruby(Rack app)
==========================

1. Enable the Phusion Passenger module

``/usr/nginx/scripts/nginx-passenger-setup.sh``

2. The above step will install rvm and a version of ruby for the modules working.
We can install any version of ruby using rvm
::

  root@cpanel1 [~]# type rvm|head -1

  rvm is a function

  [root@cpanel ~]# rvm list
  Warning! PATH is not properly set up, '/usr/local/rvm/gems/ruby-2.3.0/bin' is not at first place,
           usually this is caused by shell initialization files - check them for 'PATH=...' entries,
           it might also help to re-add RVM to your dotfiles: 'rvm get stable --auto-dotfiles',
           to fix temporarily in this shell session run: 'rvm use ruby-2.3.0'.

  rvm rubies

    ruby-2.0.0-p648 [ x86_64 ]
    ruby-2.2.4 [ x86_64 ]
  =* ruby-2.3.0 [ x86_64 ]

  # => - current
  # =* - current && default
  #  * - default

3. install bundler for all the rubies so users can run bundle install. For example
::

  rvm use ruby-2.0.0-p648
  gem install bundler

4. Register the Ruby backend using the command

  ``root@cpanel1 [~]# /opt/nDeploy/scripts/update_backend.py RUBY ruby-2.1.4 /usr/local/rvm/wrappers/ruby-2.1.4/ruby``

5. cPanel users can install more gems to local folders using
::

  bundle install --path vendor/bundle
  or
  bundle install --deployment

.. disqus::
