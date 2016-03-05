#!/usr/bin/env bash

apt-get install -y python-qt4 libqt4-webkit xvfb flashplugin-installer python-pip
cd /
mkdir /python-webkit2png
git clone https://github.com/AlexeyManikin/python-webkit2png.git python-webkit2png
cd python-webkit2png
python setup.py install
