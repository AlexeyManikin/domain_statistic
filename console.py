# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__author__ = 'alexeyymanikin'


import sys
import os
import time

PROGRAM_NAME = 'console'
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, CURRENT_DIR)
logfile = os.path.join(CURRENT_DIR, '%s.debug' % (PROGRAM_NAME))

import traceback
import time
import pprint
from classes.downloader import Downloader
from classes.converter import Converter


class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print "Elapsed time: {:.3f} sec".format(time.time() - self._startTime)

if __name__ == "__main__":
    try:
        #downloder = Downloader()
        #downloder.download_data_for_current_date()
        path = '/ssd/dev/manikin/domain_statictic/download/2015-05-20'
        converter = Converter(path)
        converter.parce_file_rib_file_to('/ssd/dev/manikin/domain_statictic/download/2015-05-20/rib.bz2',
                                         '/ssd/dev/manikin/domain_statictic/download/2015-05-20/work/rib')
    except Exception as e:
        print "Got an exception: %s" % e.message
        print traceback.format_exc()

# EOF
