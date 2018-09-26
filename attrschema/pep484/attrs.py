#!/usr/bin/env python
# -*- coding: utf-8 -*-

from attr import Attribute
from typing import Any, Callable, NoReturn


Validator = Callable[[Any, Attribute, Any], NoReturn]
