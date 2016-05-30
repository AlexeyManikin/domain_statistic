# encoding: utf-8
# Copyright (C) 2011-2013, Stefan Schwarzer <sschwarzer@sschwarzer.net>
# See the file LICENSE for licensing terms.

"""
Help make the same code work in both Python 2 and 3.

Comments given for the Python 2 versions of the helpers apply to
the Python 3 helpers as well.
"""

from __future__ import unicode_literals

import sys


__all__ = ["int_types", "unicode_type", "bytes_type", "bytes_from_ints",
           "default_string_type"]


python_version = sys.version_info[0]


if python_version == 2:

    int_types = (int, long)

    unicode_type = unicode
    bytes_type = str

    def bytes_from_ints(int_list):
        """Return a `bytes` object from a list of integers."""
        return b"".join((chr(i) for i in int_list))

else:

    int_types = (int,)

    unicode_type = str
    bytes_type = bytes

    bytes_from_ints = bytes

# For Python 2 `str` means byte strings, for Python 3 unicode strings.
default_string_type = str

