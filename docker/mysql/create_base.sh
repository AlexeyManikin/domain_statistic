#!/usr/bin/env bash

echo "create database domain_statistic;" | mysql mysql;
echo "GRANT ALL PRIVILEGES ON domain_statistic.* TO domain_statistic@'%' IDENTIFIED BY 'domain_statisticdomain_statistic';" | mysql mysql;
echo "FLUSH PRIVILEGES;" | mysql mysql;
MYPASSWD=$RANDOM$RANDOM$RANDOM
mysqladmin -u root password $MYPASSWD;
echo "[client]" > /root/.my.cnf;
echo "password=$MYPASSWD" >> /root/.my.cnf;
mysql domain_statistic < /root/structure.sql;

echo "Done"