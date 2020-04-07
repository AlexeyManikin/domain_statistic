ALTER TABLE `domain` MODIFY `id` INT, DROP PRIMARY KEY, ADD PRIMARY KEY(`domain_name`);
ALTER TABLE `domain` DROP `id`;
ALTER TABLE `domain` DROP INDEX domain_name;


ALTER TABLE `domain_history` DROP INDEX domain_id;
ALTER TABLE `domain_history` DROP `domain_id`;


ALTER TABLE domain_statistic.`beget_domain_as_from_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_as_from_count_statistic` DROP `domain_id`;

ALTER TABLE domain_statistic.`beget_domain_as_to_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_as_to_count_statistic` DROP `domain_id`;

ALTER TABLE domain_statistic.`beget_domain_ns_from_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_ns_from_count_statistic` DROP `domain_id`;

ALTER TABLE domain_statistic.`beget_domain_ns_to_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_ns_to_count_statistic` DROP `domain_id`;

ALTER TABLE domain_statistic.`beget_domain_registrant_from_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_registrant_from_count_statistic` DROP `domain_id`;

ALTER TABLE domain_statistic.`beget_domain_registrant_to_count_statistic` DROP INDEX domain_id;
ALTER TABLE domain_statistic.`beget_domain_registrant_to_count_statistic` DROP `domain_id`;




create definer = domain_statistic@`%` trigger domain_AFTER_INSERT
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
                               nserrors, rpki, ns1_like_beget)
                           VALUE(NOW(), '2038-01-01', NEW.domain_name,
                               NEW.registrant_id, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors, NEW.rpki,  if(NEW.ns1 like '%\.beget\.%', 1, 0));
END;


create definer = domain_statistic@`%` trigger domain_BEFORE_DELETE
    before delete
    on domain
    for each row
BEGIN
  DECLARE max_id integer;
  SELECT max(id) INTO max_id FROM domain_history WHERE domain_name = OLD.domain_name;
  UPDATE domain_history SET date_end = NOW() WHERE id = max_id;
END;


create definer = root@`%` trigger domain_BEFORE_UPDATE
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
                               nserrors, rpki, ns1_like_beget)
                           VALUE(NOW(), '2038-01-01', NEW.domain_name,
                               NEW.registrant_id, NEW.tld, NEW.register_date, NEW.register_date_end,
                               NEW.free_date, NEW.delegated, NEW.a1, NEW.a2,
                               NEW.a3, NEW.a4, NEW.mx1, NEW.mx2,
                               NEW.mx3, NEW.mx4, NEW.ns1, NEW.ns2,
                               NEW.ns3, NEW.ns4, NEW.txt, NEW.asn1,
                               NEW.asn2, NEW.asn3, NEW.asn4, NEW.aaaa1,
                               NEW.aaaa2, NEW.aaaa3, NEW.aaaa4, NEW.cname,
                               NEW.nserrors, NEW.rpki, if(NEW.ns1 like '%\.beget\.%', 1, 0));
    END IF;
END;