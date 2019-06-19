#!/bin/bash

BACKUPDIR="/backup"

if [ ! -f ${BACKUPDIR} ]
then
  mkdir -p ${BACKUPDIR}
fi

# pkgacct_backup
rm -rf ${BACKUPDIR}/PKGACCT_BACKUP
if [ ! -f ${BACKUPDIR}/PKGACCT_BACKUP ]
then
  mkdir -p ${BACKUPDIR}/PKGACCT_BACKUP
fi
for CPANELUSER in $(cat /etc/domainusers|cut -d: -f1)
do
  nice --adjustment=18 /scripts/pkgacct --skiphomedir --skipbwdata --skiplogs ${CPANELUSER} ${BACKUPDIR}/PKGACCT_BACKUP/
done

# system_files


# mysql_backup

rm -rf ${BACKUPDIR}/MYSQL_BACKUP
if [ ! -f ${BACKUPDIR}/MYSQL_BACKUP ]
then
  mkdir -p ${BACKUPDIR}/MYSQL_BACKUP
fi
if [ -f /usr/bin/mariabackup ]
then
  mariabackup --backup --target-dir ${BACKUPDIR}/MYSQL_BACKUP
fi
