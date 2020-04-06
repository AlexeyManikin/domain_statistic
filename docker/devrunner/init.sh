#!/usr/bin/env bash
chmod a+x /;
set -e

echo "nameserver 8.8.8.8" > /etc/resolv.conf;
chmod 644 /etc/resolv.conf;
cd /dev && chmod 666 full null random tty urandom zero;
cat /etc/hosts | grep resolver | awk '{print "nameserver "$1}' > /etc/resolv.conf || true

/etc/init.d/ssh start;

# daemon =)
tail -f /dev/null;
