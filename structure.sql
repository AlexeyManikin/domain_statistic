DROP TABLE IF EXISTS `as_list`;
CREATE TABLE `as_list` (
  `id` int(11) NOT NULL,
  `descriptions` varchar(255) DEFAULT NULL COMMENT 'Full as descriptions',
  `country` varchar(45) DEFAULT NULL COMMENT 'Country',
  `date_register` datetime DEFAULT NULL COMMENT 'Date create',
  `organization_register` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `domain`;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_name` varchar(255) DEFAULT NULL,
  `registrant` varchar(64) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `register_date` datetime DEFAULT NULL,
  `register_date_end` datetime DEFAULT NULL,
  `free_date` datetime DEFAULT NULL,
  `delegated` enum('Y','N') DEFAULT NULL,
  `a1` varchar(16) DEFAULT NULL,
  `a2` varchar(16) DEFAULT NULL,
  `a3` varchar(16) DEFAULT NULL,
  `a4` varchar(16) DEFAULT NULL,
  `ns1` varchar(45) DEFAULT NULL,
  `ns2` varchar(45) DEFAULT NULL,
  `ns3` varchar(45) DEFAULT NULL,
  `ns4` varchar(45) DEFAULT NULL,
  `mx1` varchar(70) DEFAULT NULL,
  `mx2` varchar(70) DEFAULT NULL,
  `mx3` varchar(70) DEFAULT NULL,
  `mx4` varchar(70) DEFAULT NULL,
  `txt` varchar(255) DEFAULT NULL,
  `asn1` int(11) DEFAULT NULL,
  `asn2` int(11) DEFAULT NULL,
  `asn3` int(11) DEFAULT NULL,
  `asn4` int(11) DEFAULT NULL,
  `aaaa1` varchar(55) DEFAULT NULL,
  `aaaa2` varchar(55) DEFAULT NULL,
  `aaaa3` varchar(55) DEFAULT NULL,
  `aaaa4` varchar(55) DEFAULT NULL,
  `cname` varchar(55) DEFAULT NULL,
  `nserrors` varchar(100) DEFAULT NULL,
  `load_today` enum('Y','N') DEFAULT 'Y',
  `last_update` datetime DEFAULT NULL,
  `rpki` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_name` (`domain_name`(100)),
  KEY `registrant` (`registrant`),
  KEY `deligated` (`delegated`),
  KEY `load_today` (`load_today`),
  KEY `i_ns` (`ns1`,`ns2`,`ns3`,`ns4`),
  KEY `i_ns1` (`ns1`),
  KEY `i_ns2` (`ns2`),
  KEY `i_ns3` (`ns3`),
  KEY `i_ns4` (`ns4`),
  KEY `domain` (`domain_name`),
  KEY `i_asn` (`asn1`),
  KEY `i_asn2` (`asn2`),
  KEY `i_asn3` (`asn3`),
  KEY `i_asn4` (`asn4`),
  KEY `i_asns` (`asn1`,`asn2`,`asn3`,`asn4`),
  KEY `i_a1` (`a1`),
  KEY `i_a2` (`a2`),
  KEY `i_a3` (`a3`),
  KEY `i_a4` (`a4`),
  KEY `i_a` (`a1`,`a2`,`a3`,`a4`),
  KEY `i_tld` (`tld`),
  FULLTEXT KEY `i_ftd` (`domain_name`),
  FULLTEXT KEY `ns1_ft` (`ns1`),
  FULLTEXT KEY `ns2_ft` (`ns2`),
  FULLTEXT KEY `ns3_ft` (`ns3`),
  FULLTEXT KEY `ns4_ft` (`ns4`),
  FULLTEXT KEY `ns_all_ft` (`ns1`,`ns2`,`ns3`,`ns4`),
  FULLTEXT KEY `i_ft_tld` (`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DELIMITER ;;
DROP TRIGGER IF EXISTS `domain_statistic`.`domain_AFTER_INSERT`;
CREATE TRIGGER `domain_statistic`.`domain_AFTER_INSERT` AFTER INSERT ON `domain` FOR EACH ROW
BEGIN
    INSERT INTO domain_history(domain_id,date_start, date_end, domain_name,
                               registrant, tld, register_date, register_date_end,
                               free_date, delegated, a1, a2,
                               a3, a4, mx1, mx2,
                               mx3, mx4, ns1, ns2,
                               ns3, ns4, txt, asn1,
                               asn2, asn3, asn4, aaaa1,
                               aaaa2, aaaa3, aaaa4, cname,
                               nserrors, rpki)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.domain_name,
                               NEW.registrant, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors, NEW.rpki);
END ;;
DELIMITER ;


DELIMITER ;;
DROP TRIGGER IF EXISTS `domain_statistic`.`domain_BEFORE_UPDATE`;
CREATE TRIGGER `domain_statistic`.`domain_BEFORE_UPDATE` BEFORE UPDATE ON `domain` FOR EACH ROW
BEGIN
    DECLARE max_id integer;

    IF NEW.registrant <> OLD.registrant
       OR NEW.register_date <> OLD.register_date
       OR NEW.register_date_end <> OLD.register_date_end
       OR NEW.free_date <> OLD.free_date
       OR NEW.delegated <> OLD.delegated
       OR NEW.a1 <> OLD.a1
       OR NEW.a2 <> OLD.a2
       OR NEW.a3 <> OLD.a3
       OR NEW.a4 <> OLD.a4
       OR NEW.mx1 <> OLD.mx1
       OR NEW.mx2 <> OLD.mx2
       OR NEW.mx3 <> OLD.mx3
       OR NEW.mx4 <> OLD.mx4
       OR NEW.ns1 <> OLD.ns1
       OR NEW.ns2 <> OLD.ns2
       OR NEW.ns3 <> OLD.ns3
       OR NEW.ns4 <> OLD.ns4
       OR NEW.txt <> OLD.txt
       OR NEW.asn1 <> OLD.asn1
       OR NEW.asn2 <> OLD.asn2
       OR NEW.asn3 <> OLD.asn3
       OR NEW.asn4 <> OLD.asn4
       OR NEW.aaaa1 <> OLD.aaaa1
       OR NEW.aaaa2 <> OLD.aaaa2
       OR NEW.aaaa3 <> OLD.aaaa3
       OR NEW.aaaa4 <> OLD.aaaa4
       OR NEW.cname <> OLD.cname
       OR NEW.rpki <> OLD.rpki
    THEN
          SELECT max(id) INTO max_id FROM domain_history WHERE domain_id = OLD.id;
          UPDATE domain_history SET date_end = NOW() WHERE id = max_id;

          INSERT INTO domain_history(domain_id,date_start, date_end, domain_name,
                               registrant, tld, register_date, register_date_end,
                               free_date, delegated, a1, a2,
                               a3, a4, mx1, mx2,
                               mx3, mx4, ns1, ns2,
                               ns3, ns4, txt, asn1,
                               asn2, asn3, asn4, aaaa1,
                               aaaa2, aaaa3, aaaa4, cname,
                               nserrors, rpki)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.domain_name,
                               NEW.registrant, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors, NEW.rpki);
    END IF;
END ;;
DELIMITER ;

DELIMITER ;;
DROP TRIGGER IF EXISTS `domain_statistic`.`domain_BEFORE_DELETE`;
CREATE TRIGGER `domain_statistic`.`domain_BEFORE_DELETE` BEFORE DELETE ON `domain` FOR EACH ROW
BEGIN 
  DECLARE max_id integer;
  SELECT max(id) INTO max_id FROM domain_history WHERE domain_id = OLD.id; 
  UPDATE domain_history SET date_end = NOW() WHERE id = max_id;
END ;;
DELIMITER ;

DROP TABLE IF EXISTS `domain_history`;
CREATE TABLE `domain_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `registrant` varchar(64) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `register_date` datetime DEFAULT NULL,
  `register_date_end` datetime DEFAULT NULL,
  `free_date` datetime DEFAULT NULL,
  `delegated` enum('Y','N') DEFAULT NULL,
  `a1` varchar(16) DEFAULT NULL,
  `a2` varchar(16) DEFAULT NULL,
  `a3` varchar(16) DEFAULT NULL,
  `a4` varchar(16) DEFAULT NULL,
  `ns1` varchar(45) DEFAULT NULL,
  `ns2` varchar(45) DEFAULT NULL,
  `ns3` varchar(45) DEFAULT NULL,
  `ns4` varchar(45) DEFAULT NULL,
  `mx1` varchar(70) DEFAULT NULL,
  `mx2` varchar(70) DEFAULT NULL,
  `mx3` varchar(70) DEFAULT NULL,
  `mx4` varchar(70) DEFAULT NULL,
  `txt` varchar(255) DEFAULT NULL,
  `asn1` int(11) DEFAULT NULL,
  `asn2` int(11) DEFAULT NULL,
  `asn3` int(11) DEFAULT NULL,
  `asn4` int(11) DEFAULT NULL,
  `aaaa1` varchar(55) DEFAULT NULL,
  `aaaa2` varchar(55) DEFAULT NULL,
  `aaaa3` varchar(55) DEFAULT NULL,
  `aaaa4` varchar(55) DEFAULT NULL,
  `cname` varchar(55) DEFAULT NULL,
  `nserrors` varchar(100) DEFAULT NULL,
  `rpki` int(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `domain_id` (`domain_id`),
  KEY `period` (`date_start`, `date_end`),
  KEY `period_tld` (`date_start`, `date_end`, `tld`),
  KEY `period_tld_delegated` (`date_start`, `date_end`, `tld`, `delegated`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `regru_providers`;
CREATE TABLE `regru_providers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_create` date NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL DEFAULT '-',
  `link` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL DEFAULT 'nothosting',
  `status` varchar(255) NOT NULL DEFAULT 'noactive',
  `count_ns` int(11) NOT NULL DEFAULT '2',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `i_name` (`name`),
  KEY `i_count_ns` (`count_ns`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `regru_stat_data`;
CREATE TABLE `regru_stat_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  `value` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `provider_id` (`provider_id`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `domain_count_statistic`;
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

DROP TABLE IF EXISTS `as_count_statistic`;
CREATE TABLE `as_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq` (`date`,`asn`,`tld`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`,`tld`),
  KEY `asn` (`asn`),
  KEY `i_as_tld` (`asn`,`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `mx_count_statistic`;
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

DROP TABLE IF EXISTS `ns_count_statistic`;
CREATE TABLE `ns_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns` VARCHAR(70) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq` (`date`,`ns`,`tld`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`,`tld`),
  KEY `i_ns` (`ns`),
  KEY `i_ns_tld` (`ns`,`tld`),
  KEY `i_date_ns` (`ns`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `registrant_count_statistic`;
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

DROP TABLE IF EXISTS `a_count_statistic`;
CREATE TABLE `a_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `a` VARCHAR(16) DEFAULT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq` (`date`,`a`,`tld`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`,`tld`),
  KEY `asn` (`asn`),
  KEY `i_a` (`a`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `cname_count_statistic`;
CREATE TABLE `cname_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `cname` VARCHAR(55) DEFAULT NULL,
  `tld` varchar(32) DEFAULT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq` (`date`,`cname`,`tld`),
  KEY `date` (`date`),
  KEY `date_tld` (`date`,`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `as_domain_old_count_statistic`;
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

DROP TABLE IF EXISTS `ns_domain_old_count_statistic`;
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

DROP TABLE IF EXISTS `a_domain_old_count_statistic`;
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

DROP TABLE IF EXISTS `ns_domain_group_count_statistic`;
CREATE TABLE `ns_domain_group_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns_group` VARCHAR(70) DEFAULT NULL,
  `tld` VARCHAR(32) DEFAULT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `ns_group` (`ns_group`),
  KEY `ns_group_tld` (`ns_group`, `tld`),
  KEY `date_tld` (`date`, `tld`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `rpki`;
CREATE TABLE `rpki` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(255) NOT NULL,
  `maxLength` int(10) NOT NULL,
  `asn` int(11) NOT NULL,
  `ta`  varchar(255) NOT NULL,
  `load_today` enum('Y','N') DEFAULT 'Y',
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rpki_uniq` (`prefix`(255), `maxLength`, `asn`),
  KEY `asn` (`asn`),
  KEY `load_today` (`load_today`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `rpki_history`;
CREATE TABLE `rpki_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rpki_id` int(11) NOT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `prefix` varchar(255) NOT NULL,
  `maxLength` int(10) NOT NULL,
  `asn` int(11) NOT NULL,
  `ta`  varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rpki_id` (`rpki_id`),
  KEY `period` (`date_start`, `date_end`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


DELIMITER ;;
DROP TRIGGER IF EXISTS `domain_statistic`.`rpki_AFTER_INSERT`;
CREATE TRIGGER `domain_statistic`.`rpki_AFTER_INSERT` AFTER INSERT ON `rpki` FOR EACH ROW
BEGIN
    INSERT INTO rpki_history(rpki_id,date_start, date_end, prefix,
                               maxLength, asn, ta)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.prefix,
                               NEW.maxLength, NEW.asn, NEW.ta);
END ;;
DELIMITER ;

DELIMITER ;;
DROP TRIGGER IF EXISTS `rpki`.`rpki_BEFORE_UPDATE`;
CREATE TRIGGER `rpki`.`rpki_BEFORE_UPDATE` BEFORE UPDATE ON `rpki` FOR EACH ROW
BEGIN
    DECLARE max_id integer;

    IF NEW.prefix <> OLD.prefix
       OR NEW.maxLength <> OLD.maxLength
       OR NEW.asn <> OLD.asn
       OR NEW.ta <> OLD.ta
    THEN
          SELECT max(id) INTO max_id FROM rpki_history WHERE rpki_id = OLD.id;
          UPDATE rpki_history SET date_end = NOW() WHERE id = max_id;

          INSERT INTO rpki_history(rpki_id,date_start, date_end, prefix,
                               maxLength, asn, ta)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.prefix,
                               NEW.maxLength, NEW.asn, NEW.ta);
    END IF;
END ;;
DELIMITER ;
DELIMITER ;;
DROP TRIGGER IF EXISTS `domain_statistic`.`rpki_BEFORE_DELETE`;
CREATE TRIGGER `domain_statistic`.`rpki_BEFORE_DELETE` BEFORE DELETE ON `rpki` FOR EACH ROW
BEGIN
  DECLARE max_id integer;
  SELECT max(id) INTO max_id FROM rpki_history WHERE rpki_id = OLD.id;
  UPDATE rpki_history SET date_end = NOW() WHERE id = max_id;
END ;;
DELIMITER ;

