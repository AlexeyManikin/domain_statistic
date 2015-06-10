DROP TABLE IF EXISTS `as_list`;
CREATE TABLE `as_list` (
  `id` int(11) NOT NULL,
  `descriptions` varchar(255) DEFAULT NULL COMMENT 'Full as descriptions',
  `country` varchar(45) DEFAULT NULL,
  `date_register` datetime DEFAULT NULL,
  `organization_register` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `domain`;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `load_today` enum('Y','N') DEFAULT 'Y',
  `last_update` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_name` (`domain_name`(100)),
  KEY `registrant` (`registrant`),
  KEY `deligated` (`delegated`),
  KEY `a_row` (`a1`,`a2`,`a3`,`a4`),
  KEY `ns_row` (`ns1`,`ns2`,`ns3`,`ns4`),
  KEY `mx_row` (`mx1`,`mx2`,`mx3`,`mx4`),
  KEY `asn_row` (`asn1`,`asn2`,`asn3`,`asn4`),
  KEY `load_today` (`load_today`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DELIMITER ;;
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
                               nserrors)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.domain_name,
                               NEW.registrant, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors);
END ;;
DELIMITER ;

DELIMITER ;;
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
       OR NEW.nserrors <> OLD.nserrors
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
                               nserrors)
                           VALUE(NEW.id, NOW(), '2099-01-01', NEW.domain_name,
                               NEW.registrant, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors);
    END IF;
END ;;
DELIMITER ;
DELIMITER ;;
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
  `date_start` varchar(45) DEFAULT NULL,
  `date_end` varchar(45) DEFAULT NULL,
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
  PRIMARY KEY (`id`),
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
