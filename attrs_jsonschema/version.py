#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .generics import Schema


VERSION = re.compile(r'^http://json-schema.org/draft-(\d+)/schema#$')


def schema_version(schema: Schema) -> int:
    """
    Determine the schema version by regex-ing '$schema' property of
    the schema:

    {
        ...
        '$schema': 'http://json-schema.org/draft-(\d+)/schema#'
        ...
    }

    :param schema: schema instance
    :return: schema version
    """

    try:
        s = schema['$schema']
    except KeyError:
        raise KeyError("schema has no '$schema' property")

    m = VERSION.search(s)

    if m is None:
        raise ValueError("'$schema' property failed regex")

    return int(m.group(1))
