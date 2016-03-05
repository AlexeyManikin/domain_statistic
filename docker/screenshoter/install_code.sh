#!/usr/bin/env bash

mkdir -p /home/domain_statistic;
git clone -b master -- https://gitlab.beget.ru/amanikin/domain_statictic.git /home/domain_statistic;
rm -rf /home/domain_statistic/.git;
rm -rf /home/domain_statistic/docker;
mkdir /home/domain_statistic/download;
echo Done;