#!/usr/bin/env python
# -*- coding: utf-8 -*-

from attr import Attribute
from typing import Any, Type, Union, Mapping, Callable, NoReturn
from jsonschema import Draft3Validator as Draft3
from jsonschema import Draft4Validator as Draft4


Schema = Mapping[str, Any]

Drafts = Union[Draft4, Draft3]
DraftTypes = Type[Drafts]

Validator = Callable[[Any, Attribute, Any], NoReturn]
