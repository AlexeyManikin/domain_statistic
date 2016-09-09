#!/usr/bin/env bash
set -e

echo "nameserver 8.8.8.8" > /etc/resolv.conf;
chmod 644 /etc/resolv.conf;
cd /dev && chmod 666 full null random tty urandom zero;

cat /etc/hosts | grep resolver | awk '{print "nameserver "$1}' > /etc/resolv.conf || true

/etc/init.d/ssh start;
cron >> /root/cron;
# EOF
