-- MySQL dump 10.13  Distrib 5.6.35, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: domain_statistic
-- ------------------------------------------------------
-- Server version	5.5.5-10.3.9-MariaDB-1:10.3.9+maria~bionic

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `a_count_statistic`
--

DROP TABLE IF EXISTS `a_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `a_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `a` int(10) unsigned DEFAULT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `asn` (`asn`),
  KEY `i_a` (`a`),
  KEY `i_uniq` (`date`,`a`,`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=13451921 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `a_domain_old_count_statistic`
--

DROP TABLE IF EXISTS `a_domain_old_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `a_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `a` int(10) unsigned DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `old` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `i_a` (`a`),
  KEY `uniq_index` (`date`),
  KEY `a_tld` (`a`,`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=13091306 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `as_count_statistic`
--

DROP TABLE IF EXISTS `as_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `as_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `asn` (`asn`),
  KEY `date_tld` (`date`,`tld`)
) ENGINE=InnoDB AUTO_INCREMENT=2193954 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `as_domain_old_count_statistic`
--

DROP TABLE IF EXISTS `as_domain_old_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `as_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `asn` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `old` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `asn` (`asn`)
) ENGINE=InnoDB AUTO_INCREMENT=2073513 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `as_list`
--

DROP TABLE IF EXISTS `as_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `as_list` (
  `id` int(11) NOT NULL,
  `descriptions` varchar(255) DEFAULT NULL COMMENT 'Full as descriptions',
  `country` varchar(45) DEFAULT NULL,
  `date_register` datetime DEFAULT NULL,
  `organization_register` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_as_from_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_as_from_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_as_from_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_from` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=10955 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_as_to_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_as_to_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_as_to_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_to` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=158023 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_ns_from_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_ns_from_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_ns_from_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `ns1_from` varchar(45) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=312143 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_ns_to_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_ns_to_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_ns_to_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `ns1_to` varchar(45) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=402350 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_registrant_from_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_registrant_from_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_registrant_from_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `registrant_id_from` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`),
  KEY `FK_REGISTRANT_BEGET_FROM` (`registrant_id_from`),
  CONSTRAINT `FK_REGISTRANT_BEGET_FROM` FOREIGN KEY (`registrant_id_from`) REFERENCES `registrant` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=691545 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `beget_domain_registrant_to_count_statistic`
--

DROP TABLE IF EXISTS `beget_domain_registrant_to_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `beget_domain_registrant_to_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `registrant_id_to` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`),
  KEY `FK_REGISTRANT_BEGET_TO` (`registrant_id_to`),
  CONSTRAINT `FK_REGISTRANT_BEGET_TO` FOREIGN KEY (`registrant_id_to`) REFERENCES `registrant` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=42820 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cname_count_statistic`
--

DROP TABLE IF EXISTS `cname_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cname_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `cname` varchar(55) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=28075 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `domain_name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `registrant_id` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `register_date` datetime DEFAULT NULL,
  `register_date_end` datetime DEFAULT NULL,
  `free_date` datetime DEFAULT NULL,
  `delegated` enum('Y','N') CHARACTER SET utf8 DEFAULT NULL,
  `a1` int(10) unsigned DEFAULT NULL,
  `a2` int(10) unsigned DEFAULT NULL,
  `a3` int(10) unsigned DEFAULT NULL,
  `a4` int(10) unsigned DEFAULT NULL,
  `ns1` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `ns2` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `ns3` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `ns4` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `mx1` varchar(70) CHARACTER SET utf8 DEFAULT NULL,
  `mx2` varchar(70) CHARACTER SET utf8 DEFAULT NULL,
  `mx3` varchar(70) CHARACTER SET utf8 DEFAULT NULL,
  `mx4` varchar(70) CHARACTER SET utf8 DEFAULT NULL,
  `txt` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `asn1` int(11) DEFAULT NULL,
  `asn2` int(11) DEFAULT NULL,
  `asn3` int(11) DEFAULT NULL,
  `asn4` int(11) DEFAULT NULL,
  `aaaa1` varbinary(16) DEFAULT NULL,
  `aaaa2` varbinary(16) DEFAULT NULL,
  `aaaa3` varbinary(16) DEFAULT NULL,
  `aaaa4` varbinary(16) DEFAULT NULL,
  `cname` varchar(55) CHARACTER SET utf8 DEFAULT NULL,
  `load_today` enum('Y','N') CHARACTER SET utf8 DEFAULT 'Y',
  `last_update` datetime DEFAULT NULL,
  `rpki` int(1) DEFAULT NULL,
  PRIMARY KEY (`domain_name`),
  KEY `deligated` (`delegated`),
  KEY `load_today` (`load_today`),
  KEY `i_ns1` (`ns1`),
  KEY `i_ns2` (`ns2`),
  KEY `i_ns3` (`ns3`),
  KEY `i_ns4` (`ns4`),
  KEY `i_asn` (`asn1`),
  KEY `i_asn2` (`asn2`),
  KEY `i_asn3` (`asn3`),
  KEY `i_asn4` (`asn4`),
  KEY `i_mx1` (`mx1`),
  KEY `i_mx2` (`mx2`),
  KEY `i_mx3` (`mx3`),
  KEY `i_mx4` (`mx4`),
  KEY `i_a1` (`a1`),
  KEY `i_tld` (`tld`),
  KEY `FK_REGISTRANT` (`registrant_id`),
  FULLTEXT KEY `ns1_ft` (`ns1`),
  FULLTEXT KEY `ns2_ft` (`ns2`),
  FULLTEXT KEY `ns3_ft` (`ns3`),
  FULLTEXT KEY `ns4_ft` (`ns4`),
  CONSTRAINT `FK_REGISTRANT` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`domain_statistic`@`%`*/ /*!50003 trigger domain_AFTER_INSERT
    after insert
    on domain
    for each row
BEGIN
    INSERT INTO domain_history(date_start, date_end, domain_name,
                               registrant_id, tld, register_date, register_date_end,
                               free_date, delegated, a1, a2,
                               a3, a4, mx1, mx2,
                               mx3, mx4, ns1, ns2,
                               ns3, ns4, txt, asn1,
                               asn2, asn3, asn4, aaaa1,
                               aaaa2, aaaa3, aaaa4, cname,
                               rpki, ns1_like_beget)
                           VALUE(NOW(), '2038-01-01', NEW.domain_name,
                               NEW.registrant_id, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.rpki,  if(NEW.ns1 like '%\.beget\.%', 1, 0));
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`%`*/ /*!50003 trigger domain_BEFORE_UPDATE
    before update
    on domain
    for each row
BEGIN
    DECLARE max_id integer;

    IF not (NEW.registrant_id <=> OLD.registrant_id)
       OR not (NEW.register_date <=> OLD.register_date)
       OR not (NEW.register_date_end <=> OLD.register_date_end)
       OR not (NEW.free_date <=> OLD.free_date)
       OR not (NEW.delegated <=> OLD.delegated)
       OR not (NEW.a1 <=> OLD.a1)
       OR not (NEW.a2 <=> OLD.a2)
       OR not (NEW.a3 <=> OLD.a3)
       OR not (NEW.a4 <=> OLD.a4)
       OR not (NEW.mx1 <=> OLD.mx1)
       OR not (NEW.mx2 <=> OLD.mx2)
       OR not (NEW.mx3 <=> OLD.mx3)
       OR not (NEW.mx4 <=> OLD.mx4)
       OR not (NEW.ns1 <=> OLD.ns1)
       OR not (NEW.ns2 <=> OLD.ns2)
       OR not (NEW.ns3 <=> OLD.ns3)
       OR not (NEW.ns4 <=> OLD.ns4)
       OR not (NEW.txt <=> OLD.txt)
       OR not (NEW.asn1 <=> OLD.asn1)
       OR not (NEW.asn2 <=> OLD.asn2)
       OR not (NEW.asn3 <=> OLD.asn3)
       OR not (NEW.asn4 <=> OLD.asn4)
       OR not (NEW.aaaa1 <=> OLD.aaaa1)
       OR not (NEW.aaaa2 <=> OLD.aaaa2)
       OR not (NEW.aaaa3 <=> OLD.aaaa3)
       OR not (NEW.aaaa4 <=> OLD.aaaa4)
       OR not (NEW.cname <=> OLD.cname)
       OR not (NEW.rpki <=> OLD.rpki)
    THEN
          SELECT max(id) INTO max_id FROM domain_history WHERE domain_name = OLD.domain_name;
          UPDATE domain_history SET date_end = NOW() WHERE id = max_id;

          INSERT INTO domain_history(date_start, date_end, domain_name,
                               registrant_id, tld, register_date, register_date_end,
                               free_date, delegated, a1, a2,
                               a3, a4, mx1, mx2,
                               mx3, mx4, ns1, ns2,
                               ns3, ns4, txt, asn1,
                               asn2, asn3, asn4, aaaa1,
                               aaaa2, aaaa3, aaaa4, cname,
                               rpki, ns1_like_beget)
                           VALUE(NOW(), '2038-01-01', NEW.domain_name,
                               NEW.registrant_id, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.rpki, if(NEW.ns1 like '%\.beget\.%', 1, 0));
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'IGNORE_SPACE,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`domain_statistic`@`%`*/ /*!50003 trigger domain_BEFORE_DELETE
    before delete
    on domain
    for each row
BEGIN
  DECLARE max_id integer;
  SELECT max(id) INTO max_id FROM domain_history WHERE domain_name = OLD.domain_name;
  UPDATE domain_history SET date_end = NOW() WHERE id = max_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `domain_count_statistic`
--

DROP TABLE IF EXISTS `domain_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=5577 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain_history`
--

DROP TABLE IF EXISTS `domain_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_start` timestamp NOT NULL DEFAULT current_timestamp(),
  `date_end` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `domain_name` varchar(256) DEFAULT NULL,
  `registrant_id` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `register_date` datetime DEFAULT NULL,
  `register_date_end` datetime DEFAULT NULL,
  `free_date` datetime DEFAULT NULL,
  `delegated` enum('Y','N') DEFAULT NULL,
  `a1` int(10) unsigned DEFAULT NULL,
  `a2` int(10) unsigned DEFAULT NULL,
  `a3` int(10) unsigned DEFAULT NULL,
  `a4` int(10) unsigned DEFAULT NULL,
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
  `aaaa1` varbinary(16) DEFAULT NULL,
  `aaaa2` varbinary(16) DEFAULT NULL,
  `aaaa3` varbinary(16) DEFAULT NULL,
  `aaaa4` varbinary(16) DEFAULT NULL,
  `cname` varchar(55) DEFAULT NULL,
  `rpki` int(1) DEFAULT NULL,
  `ns1_like_beget` int(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `period` (`date_start`,`date_end`),
  KEY `domain_name` (`domain_name`),
  KEY `asn1` (`asn1`),
  KEY `ns1_like_beget` (`ns1_like_beget`),
  KEY `period_tld` (`tld`,`date_start`,`date_end`),
  KEY `FK_REGISTRANT_HISTORY` (`registrant_id`),
  CONSTRAINT `FK_REGISTRANT_HISTORY` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=252743754 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mx_count_statistic`
--

DROP TABLE IF EXISTS `mx_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mx_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `mx` varchar(70) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`)
) ENGINE=InnoDB AUTO_INCREMENT=1130662 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `netangels_domain_as_from_count_statistic`
--

DROP TABLE IF EXISTS `netangels_domain_as_from_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netangels_domain_as_from_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_from` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `netangels_domain_as_to_count_statistic`
--

DROP TABLE IF EXISTS `netangels_domain_as_to_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `netangels_domain_as_to_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_to` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=340 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ns_count_statistic`
--

DROP TABLE IF EXISTS `ns_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ns_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns` varchar(70) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `i_ns` (`ns`),
  KEY `i_ns_tld` (`ns`),
  KEY `i_date_ns` (`ns`,`date`)
) ENGINE=InnoDB AUTO_INCREMENT=9423715 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ns_domain_group_count_statistic`
--

DROP TABLE IF EXISTS `ns_domain_group_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ns_domain_group_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns_group` varchar(70) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `ns_group` (`ns_group`)
) ENGINE=InnoDB AUTO_INCREMENT=3020317 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ns_domain_old_count_statistic`
--

DROP TABLE IF EXISTS `ns_domain_old_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ns_domain_old_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `ns` varchar(70) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `old` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `ns` (`ns`)
) ENGINE=InnoDB AUTO_INCREMENT=9396429 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registrant`
--

DROP TABLE IF EXISTS `registrant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registrant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registrant` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registrant` (`registrant`)
) ENGINE=InnoDB AUTO_INCREMENT=989 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `registrant_count_statistic`
--

DROP TABLE IF EXISTS `registrant_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `registrant_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `registrant_id` int(11) DEFAULT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  `count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `FK_REGISTRANT_COUNT_STATISTIC` (`registrant_id`),
  CONSTRAINT `FK_REGISTRANT_COUNT_STATISTIC` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`) ON DELETE SET NULL ON UPDATE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=94320 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `rpki`
--

DROP TABLE IF EXISTS `rpki`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rpki` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `prefix` varchar(255) NOT NULL,
  `maxLength` int(10) NOT NULL,
  `asn` int(11) NOT NULL,
  `ta` varchar(255) NOT NULL,
  `load_today` enum('Y','N') DEFAULT 'Y',
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rpki_uniq` (`prefix`,`maxLength`,`asn`),
  KEY `asn` (`asn`),
  KEY `load_today` (`load_today`)
) ENGINE=InnoDB AUTO_INCREMENT=29152 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`domain_statistic`@`%`*/ /*!50003 TRIGGER `domain_statistic`.`rpki_AFTER_INSERT` AFTER INSERT ON `rpki` FOR EACH ROW
BEGIN
    INSERT INTO rpki_history(rpki_id,date_start, date_end, prefix,
                               maxLength, asn, ta)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.prefix,
                               NEW.maxLength, NEW.asn, NEW.ta);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`domain_statistic`@`%`*/ /*!50003 TRIGGER `domain_statistic`.`rpki_BEFORE_DELETE` BEFORE DELETE ON `rpki` FOR EACH ROW
BEGIN
  DECLARE max_id integer;
  SELECT max(id) INTO max_id FROM rpki_history WHERE rpki_id = OLD.id;
  UPDATE rpki_history SET date_end = NOW() WHERE id = max_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `rpki_history`
--

DROP TABLE IF EXISTS `rpki_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rpki_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rpki_id` int(11) NOT NULL,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `prefix` varchar(255) NOT NULL,
  `maxLength` int(10) NOT NULL,
  `asn` int(11) NOT NULL,
  `ta` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rpki_id` (`rpki_id`),
  KEY `period` (`date_start`,`date_end`)
) ENGINE=InnoDB AUTO_INCREMENT=29152 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timeweb_domain_as_from_count_statistic`
--

DROP TABLE IF EXISTS `timeweb_domain_as_from_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timeweb_domain_as_from_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_from` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1234 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `timeweb_domain_as_to_count_statistic`
--

DROP TABLE IF EXISTS `timeweb_domain_as_to_count_statistic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timeweb_domain_as_to_count_statistic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `domain_name` varchar(256) DEFAULT NULL,
  `as_to` int(11) NOT NULL,
  `tld` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `date` (`date`),
  KEY `domain_name` (`domain_name`)
) ENGINE=InnoDB AUTO_INCREMENT=2692 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'domain_statistic'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-10 14:29:17
