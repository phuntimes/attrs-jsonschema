#!/usr/bin/env python
# -*- coding: utf-8 -*-

import typing

from .documents import document
from .schema import schema

Document = typing.MutableMapping[str, typing.Any]
