#!/usr/bin/env bash
set -e
echo "nameserver 8.8.8.8" > /etc/resolv.conf
chmod 644 /etc/resolv.conf
cd /dev && chmod 666 full null random tty urandom zero

cron
# EOF