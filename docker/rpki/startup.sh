#!/usr/bin/env bash
set -e

chmod 644 /etc/resolv.conf /etc/hosts* /etc/localtime || true

( cd /dev && chmod 666 full null random tty urandom zero ) || true

chmod 711 / /etc /var/log || true
chmod 777 /tmp -R || true

cd /home/rpki-validator-app-2.23
./rpki-validator.sh start  -c /home/my-configuration.conf

