#!/bin/bash

mkdir -p /opt/ru_open_statistics/domain_lists
mkdir -p /opt/ru_open_statistics/bgp

# Download domains list
domain_types="ru su rf"

for domain_type in $domain_types
do
    echo "Download domain list for zone ${domain_type}"
    rm -f /opt/ru_open_statistics/domain_lists/${domain_type}_domains
    wget "https://partner.r01.ru/zones/${domain_type}_domains.gz" -O "/opt/ru_open_statistics/domain_lists/${domain_type}_domains.gz"
    gunzip /opt/ru_open_statistics/domain_lists/${domain_type}_domains.gz
done

echo "Download subnet to ASN translation table"

rm -f /opt/ru_open_statistics/bgp/asn.txt

# http://phpsuxx.blogspot.com/2011/12/full-bgp.html
# http://phpsuxx.blogspot.com/2011/12/libbgpdump-debian-6-squeeze.html
yesterday_date=$(date --date='1 days ago' '+%Y.%m')
yesterday_date_with_day=$(date --date='1 days ago' '+%Y%m%d')

# get routing data for yesterday at 5 o'clock 
wget http://archive.routeviews.org/bgpdata/${yesterday_date}/RIBS/rib.${yesterday_date_with_day}.0600.bz2 -O /opt/ru_open_statistics/bgp/rib.bz2

echo "Convert routing data from bgpdump to asn/prefix format"
/usr/src/ru_open_statistics/bgpdump /opt/ru_open_statistics/bgp/rib.bz2 | /usr/src/ru_open_statistics/converter.pl > /opt/ru_open_statistics/bgp/asn.txt 

# remove temp file
rm -f /opt/ru_open_statistics/bgp/rib.bz2
