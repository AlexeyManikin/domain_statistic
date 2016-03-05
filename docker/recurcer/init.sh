#!/usr/bin/env bash

set -e
echo "nameserver 127.0.0.1" > /etc/resolv.conf
chmod 644 /etc/resolv.conf
cd /dev && chmod 666 full null random tty urandom zero

/usr/sbin/pdns_recursor
# EOF