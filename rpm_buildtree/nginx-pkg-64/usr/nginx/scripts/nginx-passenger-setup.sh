if [ ! -d /usr/local/rvm/gems/ruby-2.2.3 ] ; then
        echo -e '\e[93m Setting up Phusion Passenger \e[0m'
        gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
        \curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=2.2.3
	. /usr/local/rvm/scripts/rvm
	rvm reload
fi
if [ ! -d /usr/local/rvm/gems/ruby-2.2.3/gems/passenger-5.0.20/ext/nginx ] ; then
	. /usr/local/rvm/scripts/rvm
	rvm use ruby-2.2.3
        /usr/local/rvm/rubies/ruby-2.2.3/bin/gem install passenger -v 5.0.20
        ln -s /usr/nginx/buildout /usr/local/rvm/gems/ruby-2.2.3/gems/passenger-5.0.20/
fi
sed -i 's/^#//' /etc/nginx/conf.d/passenger.conf
service nginx restart || systemctl restart nginx
