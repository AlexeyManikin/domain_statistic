#!/usr/bin/env bash
set -e

mv /dev/log /dev/log.orig       || true
ln -sf /syslog/log /dev/log     || true

chmod 644 /etc/resolv.conf /etc/hosts* /etc/localtime || true

( cd /dev && chmod 666 full null random tty urandom zero ) || true

chmod 711 / /etc /var/log || true
chmod 700 /usr/bin/gcc* /usr/bin/g++* /usr/bin/ld /usr/bin/make || true

mount -o remount,hidepid=2 /proc || true
mount -o remount,size=50% /dev/shm || true

chmod 777 /tmp -R || true

if ! find /home/mysql/ -maxdepth 0 -empty | xargs -r false; then
    exec mysqld --verbose --external-locking --delay-key-write=0 --query-cache-size=0
fi

if  find /home/mysql/ -maxdepth 0 -empty | xargs -r false; then
    echo "Create base"
    mkdir /home/mysql || true
    chmod 777 /home/mysql  || true
    mysql_install_db --basedir=/usr || true
    mysqld --verbose --external-locking --delay-key-write=0 --query-cache-size=0 &
    sleep 10
    exec /root/create_base.sh;
fi
# EOF
