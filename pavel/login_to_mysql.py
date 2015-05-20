#!/usr/bin/python

from pavel import stat_config

print "mysql -u%s -p%s -D%s" % (stat_config.db_user, stat_config.db_password, stat_config.db_name)
