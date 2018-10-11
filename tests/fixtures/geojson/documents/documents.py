#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import pytest

from pathlib import Path


PARENT = Path(__file__).parent


def generator(parent: Path):
    for path in parent.glob('*.json'):
        text = path.read_text()
        data = json.loads(text)
        yield data


@pytest.fixture(
    params=[
        pytest.param(d, id=d['type']) for d in generator(PARENT)
    ]
)
def document(request):
    return request.param
