Debian 7/...
Ununtu 14.04/...

0) Tools: apt-get install -y python-pip python-all-dev

1) oursql:
    apt-get install -y libmysqlclient-dev python-mysqldb
    pip install oursql
2) Sqlalchemy:
    pip install sqlalchemy
2) subnettree:
    apt-get install -y python-subnettree
3) PowerDNS: 
    http://phpsuxx.blogspot.ru/2011/12/powerdns-recursor-debian-squeeze.html
    apt-get install -y pdns-recursor
4) MySQL
    apt-get install mysql-server 
5) Create database:

mysql -uroot -p -e "CREATE DATABASE stat CHARSET 'utf8'";
mysql -uroot -p -e "GRANT ALL PRIVILEGES ON stat.* TO 'stat_user'@'localhost' IDENTIFIED BY 'eer6paigaus2aeGa'; FLUSH PRIVILEGES;" 

# We should use *.* because file permission os global for server
mysql -uroot -p -e "GRANT FILE PRIVILEGES ON *.* TO 'stat_user'@'localhost' IDENTIFIED BY 'eer6paigaus2aeGa'; FLUSH PRIVILEGES;"
 
