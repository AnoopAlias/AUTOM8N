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
fpm -s dir -t rpm -C ../nDeploy-unison-pkg-centos7 --vendor "PiServe Technologies" --version ${UNISON_VERSION} --iteration ${UNISON_RPM_ITER} -a $(arch) -m info@piserve.com -e --description "nDeploy custom unison package" --url http://piserve.com --conflicts unison --name unison-nDeploy .
rsync -av *.rpm root@rpm.piserve.com:/home/gnusys/public_html/CentOS/7/x86_64/
