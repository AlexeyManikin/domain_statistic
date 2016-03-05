CREATE TABLE `image_storage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_name` varchar(255) NOT NULL,
  `ip` varchar(16) NOT NULL,
  `disk_uuid` varchar(45) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  `bsize` bigint(20) NOT NULL DEFAULT '0',
  `bfree` bigint(20) NOT NULL DEFAULT '0',
  `bused` bigint(20) NOT NULL DEFAULT '0',
  `avalible` enum('Y','N') NOT NULL DEFAULT 'Y',
  `read_only` enum('Y','N') NOT NULL DEFAULT 'N',
  `time_last_image` datetime DEFAULT NULL,
  `date_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `bfree` (`bfree`),
  UNIQUE KEY `ip_disk_uuid` (`ip`,`disk_uuid`),
  UNIQUE KEY `ip_path` (`ip`,`path`),
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8

CREATE TABLE `domain_images` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `storage_id` int(11) NOT NULL,
  `file_name` varchar(255) NOT NULL,
  `size` int(11) NOT NULL,
  `date_create` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `domain_id` (`domain_id`),
  KEY `storage_id` (`storage_id`),
  UNIQUE KEY `file_name_storages` (`storage_id`,`file_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8