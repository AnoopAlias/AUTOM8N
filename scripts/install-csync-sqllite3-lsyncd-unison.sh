#!/bin/bash	
#########################################################

mkdir -p /data/build/
mkdir -p /data/sync-db/
mkdir -p /data/logs/csync2
mkdir -p /data/sync-conflicts/

cd /data/build/

wget http://autobuild.itoc.com.au/csync2/librsync-0.9.7.tar.gz
wget http://oss.linbit.com/csync2/csync2-2.0.tar.gz
wget http://www.sqlite.org/sqlite-autoconf-3070603.tar.gz
wget http://www.seas.upenn.edu/~bcpierce/unison//download/releases/stable/unison-2.48.3.tar.gz
echo " Installing dependencies and llsyncd"
yum install xinetd byacc flex gcc-c++ gnutls gnutls-devel openssl-devel openssl-static lsyncd ocaml ocaml-camlp4-devel ctags ctags-etags -y /dev/null 2>&1

tar -xzf librsync-0.9.7.tar.gz 
tar -xzf csync2-2.0.tar.gz
tar -xvf sqlite-autoconf-3070603.tar.gz
tar -xzf unison-2.48.3.tar.gz
cd sqlite-autoconf-3070603
echo "Configuring and making sqllite3 .....(This can take some time. Please hold on)"
./configure 
make
make install
cd ..
cd csync2-2.0
echo "Configuring and making csync2 .....(This can take some time. Please hold on)"
./configure  --prefix=/usr --localstatedir=/var --with-librsync-source=/data/build/librsync-0.9.7.tar.gz --sysconfdir=/etc --disable-gnutls
make && make install

cd ..
cd unison-2.48.3
make
cp unison /usr/local/sbin/
cd ..
rm -rf csync2-2.0
rm -rf librsync-0.9.7
rm -rf sqlite-autoconf-3070603
rm -rf unison-2.48.3
echo "csync2        30865/tcp" >> /etc/services

CSYNCLOC=`which csync2`

echo -e "# default: on\n# description: csync2 xinetd server\n\nservice csync2\n{\n       disable         = no\n       flags           = REUSE\n       socket_type     = stream\n       wait            = no\n       user            = root\n       group           = root\n       server          = $CSYNCLOC\n       server_args     = -i -D /data/sync-db/\n       port            = 30865\n       type            = UNLISTED\n       log_type        = FILE /data/logs/csync2/csync2-xinetd.log\n       log_on_failure  += USERID\n}\n" > /etc/xinetd.d/csync2
service xinetd restart

echo -e "# Csync2 Configuration File\n# Preconfigured using the csync2 config and install script from ITOC Autobuild service\n# -----------------------------------\n#\n# Please read the doco at:\n# http://oss.linbit.com/csync2/paper.pdf\n\nnossl * *;\n\ngroup production {\n       host wsinl1-01;\n       host wsinl2-01;\n       host (wsinl1-02);\n       host (wsinl2-02);\n\n       key /etc/csync-production-group.key;\n\n       include /etc/hosts;\n       include /etc/httpd/conf/;\n#       include /data/httpd/;\n\n#      exclude *~ .*; ## dont allow sync of files starting with a dot (.)\n       exclude *.log;\n\n       action {\n              pattern /etc/httpd/conf/httpd.conf;\n              exec \"/etc/init.d/httpd reload\";\n              logfile \"/data/logs/csync2/csync2_action.log\";\n              do-local;\n       }\n\n       backup-directory /data/sync-conflicts/;\n       backup-generations 2;\n\n       auto younger;\n}" > /etc/csync2.cfg
#echo -e "# */5 * * * * root $CSYNCLOC -x -v -D /data/sync-db/ >/dev/null 2>&1" >> /etc/crontab

clear
echo -e "----------------------------------------------------------------\n"
echo -e "\n Csync2, lsyncd and unison  Installed Successfully.\n\n"
echo -e "Additional Information:"
echo -e "    Install Location of csync2: $CSYNCLOC"
echo -e "    Example Config File: /etc/csync2.cfg"
echo -e "    xinetd configuration installed and running at: /etc/xinetd.d/csync2\n"
echo -e "DONT FORGET TO RUN THE FOLLOWING:"
echo -e "    csync2 -k /etc/csync-production-group.key"
echo -e "    If you have already created a group key (during another install), copy that off the other host\n"
echo -e "DONT FORGET TO CHANGE YOUR CRONTAB:"
echo -e "    /etc/crontab (csync2 configured to run every 5 mins)\n"
echo -e "YOU MAY WANT TO CHANGE YOUR host.conf FILE TO REFLECT THE FOLLOWING:"
echo -e "    /etc/host.conf"
echo -e "        multi on"
echo -e "        order hosts,bind\n\n"
echo -e "----------------------------------------------------------------\n\n"


