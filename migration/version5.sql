DROP TABLE IF EXISTS `domain_params_type`;
CREATE TABLE `domain_params_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(20) NOT NULL,
  `type` VARCHAR(20) default 'int',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `domain_param_int`;
CREATE TABLE `domain_param_int` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `param_type` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `last` INT(1) default 0,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NOW(),
  `value` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `period` (`date_start`, `date_end`),
  KEY `last` (`last`)
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `domain_param_string`;
CREATE TABLE `domain_param_string` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `param_type` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `last` INT(1) default 0,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NOW(),
  `value` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `period` (`date_start`, `date_end`),
  KEY `last` (`last`)
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `domain_param_text`;
CREATE TABLE `domain_param_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `param_type` int(11) NOT NULL,
  `domain_id` int(11) NOT NULL,
  `last` INT(1) default 0,
  `date_start` date DEFAULT NULL,
  `date_end` date DEFAULT NOW(),
  `value` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `period` (`date_start`, `date_end`),
  KEY `last` (`last`)
  KEY `domain_id` (`domain_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;