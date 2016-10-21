if [ ! -d /usr/local/rvm/gems/ruby-RUBY_VERSION ] ; then
        echo -e '\e[93m Setting up Phusion Passenger \e[0m'
        gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
        \curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=RUBY_VERSION
	. /usr/local/rvm/scripts/rvm
	rvm reload
fi
if [ ! -d /usr/local/rvm/gems/ruby-RUBY_VERSION/gems/passenger-PASSENGER_VERSION/ext/nginx ] ; then
	. /usr/local/rvm/scripts/rvm
	rvm use ruby-RUBY_VERSION
        /usr/local/rvm/rubies/ruby-RUBY_VERSION/bin/gem install passenger -v PASSENGER_VERSION
        yum -y --enablerepo=ndeploy install nginx-nDeploy-module-passenger
        ln -s /usr/nginx/buildout /usr/local/rvm/gems/ruby-RUBY_VERSION/gems/passenger-PASSENGER_VERSION/
fi
echo -e '\e[93m Adding a Ruby backend for nDeploy. Refer http://ndeploy.readthedocs.io/ \e[0m'
echo -e '\e[93m for adding other passenger backends like Python/NodeJS etc. \e[0m'
/opt/nDeploy/scripts/update_backend.py add RUBY ruby-RUBY_VERSION /usr/local/rvm/wrappers/ruby-RUBY_VERSION/ruby
service nginx restart || systemctl restart nginx
