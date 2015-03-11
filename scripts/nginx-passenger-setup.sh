if [ ! -d /usr/local/rvm/gems/ruby-2.2.0/gems/passenger-4.0.59/ext/nginx ] ; then
        echo -e '\e[93m Setting up Phusion Passenger \e[0m'
        gpg2 --keyserver hkp://keys.gnupg.net --recv-keys D39DC0E3
        \curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=2.2.0
        /usr/local/rvm/rubies/ruby-2.2.0/bin/gem install passenger -v 4.0.59
        ln -s /usr/nginx/buildout /usr/local/rvm/gems/ruby-2.2.0/gems/passenger-4.0.59/
fi
sed -i 's/^#//' /etc/nginx/conf.d/passenger.conf
