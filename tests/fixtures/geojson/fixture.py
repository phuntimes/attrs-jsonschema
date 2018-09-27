#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from pathlib import Path

from .. import JSONObject, JSONArray


PARENT = Path(__file__).parent


def load(filename: str, parent: Path = PARENT):
    path = Path(parent, filename)
    file = path.with_suffix('.json')
    text = file.read_text()
    data = json.loads(text)
    return data


SCHEMA: JSONObject = load('schema')
SAMPLES: JSONArray = load('samples')


@pytest.fixture
def schema():
    return SCHEMA


@pytest.fixture(
    params=[pytest.param(v, id=v['type']) for v in SAMPLES]
)
def samples(request):
    return request.param
