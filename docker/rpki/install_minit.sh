#!/usr/bin/env bash

mkdir -p /etc/minit

# This is roughly equivalent to add-apt-repository ppa:chazomaticus/minit.
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E007F6BD
echo "deb http://ppa.launchpad.net/chazomaticus/minit/ubuntu quantal main" > /etc/apt/sources.list.d/minit.list
apt-get update && apt-get upgrade -y && apt-get install -y minit # etc.

apt-get clean;
rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/*;

echo "Done"