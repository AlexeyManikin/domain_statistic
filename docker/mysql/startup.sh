#!/usr/bin/env bash
set -e

chmod 644 /etc/resolv.conf /etc/hosts* /etc/localtime || true

( cd /dev && chmod 666 full null random tty urandom zero ) || true

chmod 711 / /etc /var/log || true
chmod 777 /tmp -R || true

if ! find /home/mysql/* -maxdepth 0 -empty | xargs -r false; then
    echo "Start MySQL on exist Data"
    exec mysqld --verbose --external-locking
fi

if  find /home/mysql2/* -maxdepth 0 -empty | xargs -r false; then
    echo "Create base"
    mkdir -r /home/mysql || true
    chmod 777 /home/mysql  || true
    mysql_install_db --basedir=/usr || true
    mysqld --verbose --external-locking &
    sleep 10
    exec /root/create_base.sh;
fi
# EOF
