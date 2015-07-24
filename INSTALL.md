Debian 7/...
Ununtu 14.04/...



0) Tools: apt-get install -y python-pip python-all-dev

1) MySQLdb:
3) subnettree:
    apt-get install -y python-subnettree
4) dns.resolver:
    pip install dnspython
5) PowerDNS:
    http://phpsuxx.blogspot.ru/2011/12/powerdns-recursor-debian-squeeze.html
    apt-get install -y pdns-recursor
6) MySQL
    apt-get install mysql-server
Tune it for (my.cnf):
max_connections = 5000