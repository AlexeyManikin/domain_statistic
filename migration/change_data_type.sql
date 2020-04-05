-- Domain

SET @TRIGGER_DISABLED = 1;

ALTER TABLE `domain`
    ADD `a1_tmp` int unsigned DEFAULT NULL after a1,
    ADD `a2_tmp` int unsigned DEFAULT NULL after a2,
    ADD `a3_tmp` int unsigned DEFAULT NULL after a3,
    ADD `a4_tmp` int unsigned DEFAULT NULL after a4,
    ADD `aaaa1_tmp` VARBINARY(16) DEFAULT NULL after aaaa1,
    ADD `aaaa2_tmp` VARBINARY(16) DEFAULT NULL after aaaa2,
    ADD `aaaa3_tmp` VARBINARY(16) DEFAULT NULL after aaaa3,
    ADD `aaaa4_tmp` VARBINARY(16) DEFAULT NULL after aaaa4;

UPDATE domain
set a1_tmp = INET_ATON(a1),
    a2_tmp = INET_ATON(a2),
    a3_tmp = INET_ATON(a3),
    a4_tmp = INET_ATON(a4),
    aaaa1_tmp = INET6_ATON(aaaa1),
    aaaa2_tmp = INET6_ATON(aaaa2),
    aaaa3_tmp = INET6_ATON(aaaa3),
    aaaa4_tmp = INET6_ATON(aaaa4)
WHERE 1 = 1;

DROP INDEX i_a ON domain;
DROP INDEX i_a1 ON domain;
DROP INDEX i_a2 ON domain;
DROP INDEX i_a3 ON domain;

ALTER TABLE domain DROP a1, DROP a2, DROP a3, DROP a4, DROP aaaa1, DROP aaaa2, DROP aaaa3, DROP aaaa4;

ALTER TABLE domain CHANGE a1_tmp  a1 int unsigned DEFAULT NULL,
 CHANGE a2_tmp  a2 int unsigned DEFAULT NULL,
 CHANGE a3_tmp  a3 int unsigned DEFAULT NULL,
 CHANGE a4_tmp  a4 int unsigned DEFAULT NULL,
 CHANGE aaaa1_tmp  aaaa1  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa2_tmp  aaaa2  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa3_tmp  aaaa3  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa4_tmp  aaaa4  VARBINARY(16) DEFAULT NULL;

CREATE INDEX i_a ON domain (a1, a2, a3, a4);
CREATE INDEX i_a1 ON domain (a1);

DROP INDEX domain ON domain;
DROP INDEX i_ft_tld ON domain;
DROP INDEX i_ftd on domain;


-- Domain history

ALTER TABLE `domain_history`
    ADD `a1_tmp` int unsigned DEFAULT NULL after a1,
    ADD `a2_tmp` int unsigned DEFAULT NULL after a2,
    ADD `a3_tmp` int unsigned DEFAULT NULL after a3,
    ADD `a4_tmp` int unsigned DEFAULT NULL after a4,
    ADD `aaaa1_tmp` VARBINARY(16) DEFAULT NULL after aaaa1,
    ADD `aaaa2_tmp` VARBINARY(16) DEFAULT NULL after aaaa2,
    ADD `aaaa3_tmp` VARBINARY(16) DEFAULT NULL after aaaa3,
    ADD `aaaa4_tmp` VARBINARY(16) DEFAULT NULL after aaaa4;

UPDATE domain_history
set a1_tmp = INET_ATON(a1),
    a2_tmp = INET_ATON(a2),
    a3_tmp = INET_ATON(a3),
    a4_tmp = INET_ATON(a4),
    aaaa1_tmp = INET6_ATON(aaaa1),
    aaaa2_tmp = INET6_ATON(aaaa2),
    aaaa3_tmp = INET6_ATON(aaaa3),
    aaaa4_tmp = INET6_ATON(aaaa4)
WHERE 1 = 1;

ALTER TABLE domain_history DROP a1, DROP a2, DROP a3, DROP a4, DROP aaaa1, DROP aaaa2, DROP aaaa3, DROP aaaa4;

ALTER TABLE domain_history CHANGE a1_tmp  a1 int unsigned DEFAULT NULL,
 CHANGE a2_tmp  a2 int unsigned DEFAULT NULL,
 CHANGE a3_tmp  a3 int unsigned DEFAULT NULL,
 CHANGE a4_tmp  a4 int unsigned DEFAULT NULL,
 CHANGE aaaa1_tmp  aaaa1  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa2_tmp  aaaa2  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa3_tmp  aaaa3  VARBINARY(16) DEFAULT NULL,
 CHANGE aaaa4_tmp  aaaa4  VARBINARY(16) DEFAULT NULL;

-- a_count_statistic

ALTER TABLE `a_count_statistic`
    ADD `a_tmp` int unsigned DEFAULT NULL after a;

DROP INDEX i_a ON a_count_statistic;
DROP INDEX uniq ON a_count_statistic;
UPDATE a_count_statistic
    set a_tmp = INET_ATON(a)
WHERE 1=1;
ALTER TABLE a_count_statistic DROP a;
ALTER TABLE a_count_statistic CHANGE a_tmp  a int unsigned DEFAULT NULL;

CREATE INDEX i_a ON a_count_statistic (a);
CREATE INDEX uniq_index ON a_count_statistic (tld, date);


-- a_domain_old_count_statistic

ALTER TABLE `a_domain_old_count_statistic`
    ADD `a_tmp` int unsigned DEFAULT NULL after a;

DROP INDEX a ON a_domain_old_count_statistic;
DROP INDEX a_tld ON a_domain_old_count_statistic;

UPDATE a_domain_old_count_statistic
    set a_tmp = INET_ATON(a)
WHERE 1=1;

ALTER TABLE a_domain_old_count_statistic DROP a;
ALTER TABLE a_domain_old_count_statistic CHANGE a_tmp  a int unsigned DEFAULT NULL;

CREATE INDEX i_a ON a_domain_old_count_statistic (a);
CREATE INDEX uniq_index ON a_domain_old_count_statistic (tld, date);

-- change tld
ALTER TABLE `domain` ADD `tld_tmp` TINYINT unsigned not null after tld;
UPDATE domain SET domain.tld_tmp = 0 WHERE tld = 'ru';
UPDATE domain SET domain.tld_tmp = 1 WHERE tld = 'su';
UPDATE domain SET domain.tld_tmp = 2 WHERE tld = 'rf';

DROP INDEX i_ft_tld ON domain;
DROP INDEX i_tld ON domain;

ALTER TABLE domain DROP tld;
ALTER TABLE domain CHANGE tld_tmp  tld TINYINT unsigned not null;
CREATE INDEX i_tld ON domain (tld);

ALTER TABLE `domain_history` ADD `tld_tmp` TINYINT unsigned not null after tld;
UPDATE domain_history SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE domain_history SET tld_tmp = 1 WHERE tld = 'su';
UPDATE domain_history SET tld_tmp = 2 WHERE tld = 'rf';

DROP INDEX period_tld ON domain_history;
DROP INDEX period_tld_delegated ON domain_history;

ALTER TABLE domain_history DROP tld;
ALTER TABLE domain_history CHANGE tld_tmp  tld TINYINT unsigned not null;

CREATE INDEX period_tld ON domain_history (tld, date_start, date_end);

-- a_count_statistic

ALTER TABLE a_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX uniq ON a_count_statistic;
DROP INDEX date_tld ON a_count_statistic;

UPDATE a_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE a_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE a_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE a_count_statistic DROP tld;
ALTER TABLE a_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

CREATE INDEX i_uniq ON a_count_statistic (date, a ,tld);

-- a_domain_old_count_statistic

ALTER TABLE a_domain_old_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX a_tld ON a_domain_old_count_statistic;
DROP INDEX date_tld ON a_domain_old_count_statistic;

UPDATE a_domain_old_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE a_domain_old_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE a_domain_old_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE a_domain_old_count_statistic DROP tld;
ALTER TABLE a_domain_old_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

CREATE INDEX a_tld ON a_domain_old_count_statistic (a ,tld);


-- a_domain_old_count_statistic

ALTER TABLE as_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX i_as_tld ON as_count_statistic;
DROP INDEX date_tld ON as_count_statistic;
DROP INDEX uniq ON as_count_statistic;

UPDATE as_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE as_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE as_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE as_count_statistic DROP tld;
ALTER TABLE as_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

CREATE INDEX date_tld ON as_count_statistic (date, tld);

-- as_domain_old_count_statistic

ALTER TABLE as_domain_old_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX asn_tld ON as_domain_old_count_statistic;
DROP INDEX date_tld ON as_domain_old_count_statistic;

UPDATE as_domain_old_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE as_domain_old_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE as_domain_old_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE as_domain_old_count_statistic DROP tld;
ALTER TABLE as_domain_old_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

-- beget_domain*

ALTER TABLE beget_domain_as_from_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;
ALTER TABLE beget_domain_as_to_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;
ALTER TABLE beget_domain_ns_from_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;
ALTER TABLE beget_domain_ns_to_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;



DROP INDEX tld ON beget_domain_as_from_count_statistic;
DROP INDEX tld ON beget_domain_as_to_count_statistic;
DROP INDEX tld ON beget_domain_ns_from_count_statistic;
DROP INDEX tld ON beget_domain_ns_to_count_statistic;


UPDATE beget_domain_as_from_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE beget_domain_as_from_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE beget_domain_as_from_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

UPDATE beget_domain_as_to_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE beget_domain_as_to_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE beget_domain_as_to_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

UPDATE beget_domain_ns_from_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE beget_domain_ns_from_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE beget_domain_ns_from_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

UPDATE beget_domain_ns_to_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE beget_domain_ns_to_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE beget_domain_ns_to_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';



ALTER TABLE beget_domain_as_from_count_statistic DROP tld;
ALTER TABLE beget_domain_as_from_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

ALTER TABLE beget_domain_as_to_count_statistic DROP tld;
ALTER TABLE beget_domain_as_to_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

ALTER TABLE beget_domain_ns_from_count_statistic DROP tld;
ALTER TABLE beget_domain_ns_from_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

ALTER TABLE beget_domain_ns_to_count_statistic DROP tld;
ALTER TABLE beget_domain_ns_to_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;


--

-- cname_count_statistic

ALTER TABLE cname_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON cname_count_statistic;
DROP INDEX uniq ON cname_count_statistic;

UPDATE cname_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE cname_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE cname_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE cname_count_statistic DROP tld;
ALTER TABLE cname_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;


-- domain_count_statistic

ALTER TABLE domain_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON domain_count_statistic;
DROP INDEX uniq ON domain_count_statistic;

UPDATE domain_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE domain_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE domain_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE domain_count_statistic DROP tld;
ALTER TABLE domain_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

-- mx_count_statistic

ALTER TABLE mx_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON mx_count_statistic;
DROP INDEX uniq ON mx_count_statistic;

UPDATE mx_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE mx_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE mx_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE mx_count_statistic DROP tld;
ALTER TABLE mx_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;


-- ns_count_statistic

ALTER TABLE ns_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON ns_count_statistic;
DROP INDEX uniq ON ns_count_statistic;

UPDATE ns_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE ns_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE ns_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE ns_count_statistic DROP tld;
ALTER TABLE ns_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;


-- ns_count_statistic

ALTER TABLE ns_domain_group_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON ns_domain_group_count_statistic;
DROP INDEX ns_group_tld ON ns_domain_group_count_statistic;

UPDATE ns_domain_group_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE ns_domain_group_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE ns_domain_group_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE ns_domain_group_count_statistic DROP tld;
ALTER TABLE ns_domain_group_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;


-- ns_domain_old_count_statistic

ALTER TABLE ns_domain_old_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON ns_domain_old_count_statistic;
DROP INDEX ns_tld ON ns_domain_old_count_statistic;

UPDATE ns_domain_old_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE ns_domain_old_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE ns_domain_old_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE ns_domain_old_count_statistic DROP tld;
ALTER TABLE ns_domain_old_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;



-- registrant_count_statistic

ALTER TABLE registrant_count_statistic
    ADD `tld_tmp`  TINYINT unsigned not null after tld;

DROP INDEX date_tld ON registrant_count_statistic;
DROP INDEX uniq ON registrant_count_statistic;

UPDATE registrant_count_statistic SET tld_tmp = 0 WHERE tld = 'ru';
UPDATE registrant_count_statistic SET tld_tmp = 1 WHERE tld = 'su';
UPDATE registrant_count_statistic SET tld_tmp = 2 WHERE tld = 'rf';

ALTER TABLE registrant_count_statistic DROP tld;
ALTER TABLE registrant_count_statistic CHANGE tld_tmp  tld  TINYINT unsigned not null;

drop table regru_providers;
drop table regru_stat_data;

CREATE TABLE `registrant` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `registrant` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `registrant` (`registrant`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=latin1;

insert into registrant(registrant) select distinct registrant from domain_history;


SET @foreign_key_checks=0;
SET foreign_key_checks=0;

ALTER TABLE domain ADD `registrant_id` int(11) DEFAULT NULL after registrant;
UPDATE domain as d set d.registrant_id = (SELECT r.id from registrant as r where r.registrant = d.registrant) WHERE 1 = 1;
ALTER TABLE `domain` ADD CONSTRAINT `FK_REGISTRANT` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`)  ON DELETE SET NULL ON UPDATE SET NULL;
DROP INDEX registrant ON domain;
ALTER TABLE domain DROP registrant;


ALTER TABLE domain_history ADD `registrant_id` int(11) DEFAULT NULL after registrant;
UPDATE domain_history as d set d.registrant_id = (SELECT r.id from registrant as r where r.registrant = d.registrant) WHERE 1 = 1;
ALTER TABLE `domain_history` ADD CONSTRAINT `FK_REGISTRANT_HISTORY` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`)  ON DELETE SET NULL ON UPDATE SET NULL;
DROP INDEX registrant ON domain_history;
ALTER TABLE domain_history DROP registrant;



ALTER TABLE registrant_count_statistic ADD `registrant_id` int(11) DEFAULT NULL after registrant;
UPDATE registrant_count_statistic as d set d.registrant_id = (SELECT r.id from registrant as r where r.registrant = d.registrant) WHERE 1 = 1;
ALTER TABLE `registrant_count_statistic` ADD CONSTRAINT `FK_REGISTRANT_COUNT_STATISTIC` FOREIGN KEY (`registrant_id`) REFERENCES `registrant` (`id`)  ON DELETE SET NULL ON UPDATE SET NULL;
ALTER TABLE registrant_count_statistic DROP registrant;


ALTER TABLE beget_domain_registrant_from_count_statistic ADD `registrant_id_from` int(11) DEFAULT NULL after registrant_from;
UPDATE beget_domain_registrant_from_count_statistic as d set d.registrant_id_from = (SELECT r.id from registrant as r where r.registrant = d.registrant_from) WHERE 1 = 1;
ALTER TABLE `beget_domain_registrant_from_count_statistic` ADD CONSTRAINT `FK_REGISTRANT_BEGET_FROM` FOREIGN KEY (`registrant_id_from`) REFERENCES `registrant` (`id`)  ON DELETE SET NULL ON UPDATE SET NULL;
ALTER TABLE beget_domain_registrant_from_count_statistic DROP registrant_from;


ALTER TABLE beget_domain_registrant_to_count_statistic ADD `registrant_id_to` int(11) DEFAULT NULL after registrant_to;
UPDATE beget_domain_registrant_to_count_statistic as d set d.registrant_id_to = (SELECT r.id from registrant as r where r.registrant = d.registrant_to) WHERE 1 = 1;
ALTER TABLE `beget_domain_registrant_to_count_statistic` ADD CONSTRAINT `FK_REGISTRANT_BEGET_TO` FOREIGN KEY (`registrant_id_to`) REFERENCES `registrant` (`id`)  ON DELETE SET NULL ON UPDATE SET NULL;
ALTER TABLE beget_domain_registrant_to_count_statistic DROP registrant_to;

