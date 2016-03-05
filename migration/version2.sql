ALTER TABLE `domain` MODIFY `domain_name` varchar(255) DEFAULT NULL;
ALTER TABLE `domain` ADD fulltext INDEX `i_ftd` (`domain_name`);