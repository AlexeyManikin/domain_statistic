#!/usr/bin/env bash

echo "create database domain_statistic;" | mysql mysql;
echo "GRANT ALL PRIVILEGES ON domain_statistic.* TO domain_statistic@'%' IDENTIFIED BY '12345678';" | mysql mysql;
echo "GRANT SELECT ON domain_statistic.* TO readonlyqweqweqwe@'%' IDENTIFIED BY 'readonlyqweqweqwe';" | mysql mysql;
echo "FLUSH PRIVILEGES;" | mysql mysql;
MYPASSWD=$RANDOM$RANDOM$RANDOM
mysqladmin -u root password $MYPASSWD;
echo "[client]" > /root/.my.cnf;
echo "password=$MYPASSWD" >> /root/.my.cnf;
mysql domain_statistic < /root/structure.sql;

echo "Done"