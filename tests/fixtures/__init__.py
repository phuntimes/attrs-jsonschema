#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import MutableMapping, MutableSequence, Any

JSONObject = MutableMapping[str, Any]
JSONArray = MutableSequence[JSONObject]
