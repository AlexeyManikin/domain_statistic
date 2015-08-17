#!/bin/bash
set -e

mv /dev/log /dev/log.orig       || true
ln -sf /syslog/log /dev/log     || true

mv /etc/passwd /etc/passwd.orig || true
ln -sf /nss/passwd /etc/passwd  || true

mv /etc/group /etc/group.orig   || true
ln -sf /nss/group /etc/group    || true

chmod 644 /etc/resolv.conf /etc/hosts* /etc/localtime || true

( cd /dev && chmod 666 full null random tty urandom zero ) || true

chmod 711 / /etc /var/log || true
chmod 700 /usr/bin/gcc* /usr/bin/g++* /usr/bin/ld /usr/bin/make || true

mount -o remount,hidepid=2 /proc || true
mount -o remount,size=50% /dev/shm || true

if ! find /home/mysql/ -maxdepth 0 -empty | xargs -r false; then
    mysql_install_db --basedir=/usr || true
    echo "create database domain_statistic;" | mysql mysql;
    echo "GRANT ALL PRIVILEGES ON domain_statistic.* TO domain_statistic@localhost IDENTIFIED BY 'domain_statisticdomain_statistic';" | mysql mysql;
    echo "FLUSH PRIVILEGES;" | mysql mysql;
    cat /root/stricture.sql | mysql domain_statistic;
    MYPASSWD=$RANDOM$RANDOM$RANDOM
    mysqladmin -u root password $MYPASSWD;
    echo "[client]" > /root/.my.cnf;
    echo "password = $MYPASSWD" >> /root/.my.cnf;
fi

exec mysqld --verbose --external-locking --delay-key-write=0 --query-cache-size=0
# EOF
