Install:

* Install dependencies with this [guide](https://github.com/pavel-odintsov/ru_open_statistics/blob/master/INSTALL)
* Install code:
```bash
cd /usr/src
git clone https://github.com/pavel-odintsov/ru_open_statistics.git
```

Usage:

* Download data (domain lists and asn/subnet mapping): ./download_raw_data.sh
* Create database (drop all tables and create new): ./stat_sync_scheme.py
* Load domain listings to mysql: ./stat_load_data.py
* Resolve and postprocess domains: ./stat_resolve_domains.py
* Graph data: ./stat_report.py 

Example statistics generated at 16 sep 2014: [stats](https://github.com/pavel-odintsov/ru_open_statistics/wiki/%D0%A1%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0-%D0%B7%D0%BE%D0%BD%D1%8B-.RU-%D0%B7%D0%B0-16-%D1%81%D0%B5%D0%BD%D1%82%D1%8F%D0%B1%D1%80%D1%8F-2014)

