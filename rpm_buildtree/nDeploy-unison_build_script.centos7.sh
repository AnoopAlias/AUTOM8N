#!/bin/bash
UNISON_VERSION="2.48.4"
UNISON_RPM_ITER="1.el7"

yum install ocaml ocaml-ssl-devel
rm -rf unison-*
rm -f nDeploy-unison-pkg-centos7/usr/bin/unison*
rm -f nDeploy-unison-pkg-centos7/*.rpm
wget http://www.seas.upenn.edu/~bcpierce/unison//download/releases/stable/unison-${UNISON_VERSION}.tar.gz
tar -xvzf unison-${UNISON_VERSION}.tar.gz
mv src unison-${UNISON_VERSION}
cd unison-${UNISON_VERSION}
make UISTYLE=text NATIVE=true STATIC=true
mkdir -p ../nDeploy-unison-pkg-centos7/usr/bin
rsync -av unison ../nDeploy-unison-pkg-centos7/usr/bin/
cd ../nDeploy-unison-pkg-centos7
fpm -s dir -t rpm -C ../nDeploy-unison-pkg-centos7 --vendor "Anoop P Alias" --version ${UNISON_VERSION} --iteration ${UNISON_RPM_ITER} -a $(arch) -m anoopalias01@gmail.com -e --description "nDeploy custom unison package" --url http://anoopalias.github.io/XtendWeb/ --conflicts unison --name unison-nDeploy .
rsync -av *.rpm root@autom8n.com:/usr/share/nginx/autom8n/CentOS/7/x86_64/
