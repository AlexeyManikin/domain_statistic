ALTER TABLE `domain` ADD rpki int(1) DEFAULT NULL;
ALTER TABLE `domain_history` ADD rpki int(1) DEFAULT NULL;

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

