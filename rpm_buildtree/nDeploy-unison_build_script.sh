#!/bin/bash
UNISON_VERSION="2.48.3"
UNISON_RPM_ITER="2.el6"

yum install ocaml ocaml-ssl-devel
mkdir nDeploy-unison-pkg
rm -rf unison-*
rm -f nDeploy-unison-pkg/usr/bin/unison*
rm -f nDeploy-unison-pkg/*.rpm
wget http://www.seas.upenn.edu/~bcpierce/unison//download/releases/stable/unison-${UNISON_VERSION}.tar.gz
tar -xvzf unison-${UNISON_VERSION}.tar.gz
cd unison-${UNISON_VERSION}
make UISTYLE=text NATIVE=true STATIC=true
mkdir -p ../nDeploy-unison-pkg/usr/bin
rsync -av unison ../nDeploy-unison-pkg/usr/bin/
cd ../nDeploy-unison-pkg
fpm -s dir -t rpm -C ../nDeploy-unison-pkg --vendor "PiServe Technologies" --version ${UNISON_VERSION} --iteration ${UNISON_RPM_ITER} --rpm-sign -a $(arch) -m info@piserve.com -e --description "nDeploy custom unison package" --url http://piserve.com --conflicts unison --name unison-nDeploy .
rsync -av *.rpm root@rpm.piserve.com:/home/rpmrepo/public_html/CentOS/6/x86_64/
