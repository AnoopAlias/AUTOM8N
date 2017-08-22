if [ ! -d /usr/local/rvm/gems/ruby-RUBY_VERSION ] ; then
        echo -e '\e[93m Setting up Phusion Passenger \e[0m'
        echo -e '\e[93m Setting up Ruby. Grab a coffee as this is going to take a while \e[0m'
        gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
        # \curl -sSL https://get.rvm.io | sudo bash -s stable --ruby=RUBY_VERSION  #https://github.com/rvm/rvm/issues/4068
        \curl -sSL https://raw.githubusercontent.com/wayneeseguin/rvm/stable/binscripts/rvm-installer | sudo bash -s stable --ruby=RUBY_VERSION
	. /usr/local/rvm/scripts/rvm
	rvm reload
fi
if [ ! -d /usr/local/rvm/gems/ruby-RUBY_VERSION/gems/passenger-PASSENGER_VERSION/ext/nginx ] ; then
	. /usr/local/rvm/scripts/rvm
	rvm use ruby-RUBY_VERSION
        /usr/local/rvm/rubies/ruby-RUBY_VERSION/bin/gem install passenger -v PASSENGER_VERSION
        ln -s /usr/nginx/buildout /usr/local/rvm/gems/ruby-RUBY_VERSION/gems/passenger-PASSENGER_VERSION/
fi
echo -e '\e[93m Adding a Ruby backend for XtendWeb.  \e[0m'
/opt/nDeploy/scripts/update_backend.py add RUBY ruby-RUBY_VERSION /usr/local/rvm/wrappers/ruby-RUBY_VERSION/ruby
echo -e '\e[93m Installing bundler  \e[0m'
/usr/local/rvm/rubies/ruby-RUBY_VERSION/bin/gem install bundler

echo -e '\e[93m Setting up Python. Grab a coffee as this is going to take a while \e[0m'
curl -kL https://raw.github.com/saghul/pythonz/master/pythonz-install | bash
/usr/local/pythonz/bin/pythonz install 2.7
echo -e '\e[93m Adding a Python backend for XtendWeb.  \e[0m'
/opt/nDeploy/scripts/update_backend.py add PYTHON CPython-2.7 /usr/local/pythonz/pythons/CPython-2.7/bin/python
echo -e '\e[93m Bootstrapping pip  \e[0m'
curl https://bootstrap.pypa.io/get-pip.py | /usr/local/pythonz/pythons/CPython-2.7/bin/python

export NVM_DIR="/usr/local/nvm"
echo -e '\e[93m Setting up NodeJS. Grab a coffee as this is going to take a while \e[0m'
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
export NVM_DIR="/usr/local/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install v6.10.1
echo -e '\e[93m Adding a NodeJS backend for XtendWeb.  \e[0m'
/opt/nDeploy/scripts/update_backend.py add NODEJS v6.10.1 /usr/local/nvm/versions/node/v6.10.1/bin/node
nginx -s reload
echo -e '\e[93m Additional versions of Ruby/Python/NodeJS can be installed by following docs at.  \e[0m'
echo -e '\e[93m https://autom8n.com/xtendweb  \e[0m'
