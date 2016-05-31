CREATE TABLE `as_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` VARCHAR(32) DEFAULT NULL,
  `old` FLOAT(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `asn` (`asn`),
  KEY `asn_tld` (`asn`, `tld`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
