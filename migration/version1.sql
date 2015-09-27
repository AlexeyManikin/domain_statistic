DROP INDEX `a_row` ON `domain`;
DROP INDEX `ns_row` ON `domain`;
DROP INDEX `mx_row` ON `domain`;
DROP INDEX `asn_row` ON `domain`;

ALTER TABLE `domain_history` ADD INDEX `period_tld` (`date_start`, `date_end`, `tld`);
ALTER TABLE `domain_history` ADD INDEX `period_tld_delegated` (`date_start`, `date_end`, `tld`, `delegated`);

CREATE TABLE `domain_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `tld` VARCHAR(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `as_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `asn`, `tld`),
  KEY asn (`asn`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `mx_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `mx` VARCHAR(70) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `mx`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `ns_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns` VARCHAR(70) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `ns`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `registrant_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `registrant` VARCHAR(70) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `registrant`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `a_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `a` VARCHAR(16) DEFAULT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `a`, `tld`),
  KEY asn (`asn`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `cname_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `cname` VARCHAR(55) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`, `tld`),
  UNIQUE KEY `uniq` (`date`, `cname`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;