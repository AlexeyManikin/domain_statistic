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
  KEY `date_tld` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `ns_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns` VARCHAR(70) DEFAULT NULL,
  `tld` VARCHAR(32) DEFAULT NULL,
  `old` FLOAT(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `ns` (`ns`),
  KEY `ns_tld` (`ns`, `tld`),
  KEY `date_tld` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `a_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `a` VARCHAR(16) DEFAULT NULL,
  `tld` VARCHAR(32) DEFAULT NULL,
  `old` FLOAT(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `a` (`a`),
  KEY `a_tld` (`a`, `tld`),
  KEY `date_tld` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
