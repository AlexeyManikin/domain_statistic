# Copyright (C) 2013, Stefan Schwarzer
# See the file LICENSE for licensing terms.

"""
tool.py - helper code
"""

from __future__ import unicode_literals

import compat as compat


__all__ = ["same_string_type_as", "as_bytes", "as_unicode",
           "as_default_string"]


# Encoding to convert between byte string and unicode string. This is
# a "lossless" encoding: Strings can be encoded/decoded back and forth
# without information loss or causing encoding-related errors. The
# `ftplib` module under Python 3 also uses the "latin1" encoding
# internally. It's important to use the same encoding here, so that users who
# used `ftplib` to create FTP items with non-ASCII characters can access them
# in the same way with ftputil.
LOSSLESS_ENCODING = "utf-8"



def same_string_type_as(type_source, content_source):
    """
    Return a string of the same type as `type_source` with the content
    from `content_source`.

    If the `type_source` and `content_source` don't have the same
    type, use `LOSSLESS_ENCODING` above to encode or decode, whatever
    operation is needed.
    """
    if (
      isinstance(type_source, compat.bytes_type) and
      isinstance(content_source, compat.unicode_type)):
        return content_source.encode(LOSSLESS_ENCODING)
    elif (
      isinstance(type_source, compat.unicode_type) and
      isinstance(content_source, compat.bytes_type)):
        return content_source.decode(LOSSLESS_ENCODING)
    else:
        return content_source


def as_bytes(string):
    """
    Return the argument `string` converted to a byte string if it's a
    unicode string. Otherwise just return the string.
    """
    return same_string_type_as(b"", string)


def as_unicode(string):
    """
    Return the argument `string` converted to a unicode string if it's
    a byte string. Otherwise just return the string.
    """
    return same_string_type_as("", string)


def as_default_string(string):
    """
    Return the argument `string` converted to a the default string
    type for the Python version. For unicode strings,
    `LOSSLESS_ENCODING` is used for encoding or decoding.
    """
    return same_string_type_as(compat.default_string_type(), string)


def encode_if_unicode(string, encoding):
    """
    Return the string `string`, encoded with `encoding` if `string` is
    a unicode string. Otherwise return `string` unchanged.
    """
    if isinstance(string, compat.unicode_type):
        return string.encode(encoding)
    else:
        return string


def recursive_str_to_unicode(target):
    """
    recursive function for convert all string in dict, tuple and list to unicode
    """
    pack_result = []

    if isinstance(target, dict):
        level = {}
        for key, val in target.iteritems():
            ukey = recursive_str_to_unicode(key)
            uval = recursive_str_to_unicode(val)
            level[ukey] = uval
        pack_result.append(level)
    elif isinstance(target, list):
        level = []
        for leaf in target:
            uleaf = recursive_str_to_unicode(leaf)
            level.append(uleaf)
        pack_result.append(level)
    elif isinstance(target, tuple):
        level = []
        for leaf in target:
            uleaf = recursive_str_to_unicode(leaf)
            level.append(uleaf)
        pack_result.append(tuple(level))
    elif isinstance(target, str):
        return as_unicode(target)
    else:
        return target

    result = pack_result.pop()
    return result


################################################################################
# Testing

if __name__ == '__main__':
    test_obj = {str('myList'): [str('inList1'), str('inList2')],
                str('myTuple'): (str('inTuple1'), str('inTuple2')),
                str('mystr'): str('text'),
                str('myint'): 99}
    print repr(test_obj)
    print repr(recursive_str_to_unicode(test_obj))