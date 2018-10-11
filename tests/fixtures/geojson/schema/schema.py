#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from pathlib import Path


@pytest.fixture
def schema():
    path = Path(__file__).with_suffix('.json')
    text = path.read_text()
    data = json.loads(text)
    return data
