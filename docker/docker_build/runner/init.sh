#!/bin/bash
set -e

( cd /etc && chmod 644 resolv.conf /etc/hosts* /etc/localtime ) || true
( cd /dev && chmod 666 full null random tty urandom zero      ) || true

chmod 711 / /etc/ /var/log/                                     || true

echo "nameserver 127.0.0.1" > /etc/resolv.conf
chmod 644 /etc/resolv.conf

/usr/sbin/pdns_recursor
cron
# EOF
