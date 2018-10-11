#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import typing

from jsonschema import Draft4Validator, Draft3Validator

from . import Schema, Document


Draft = typing.Union[Draft4Validator, Draft3Validator]
DraftType = typing.Type[Draft]


@pytest.fixture(
    params=[
        pytest.param(Draft4Validator, id='Draft4'),
        pytest.param(Draft4Validator, id='Draft3')
    ]
)
def validator(request, schema: Schema):
    cls: DraftType = request.param
    return cls(schema)


def test_schema(validator: Draft):
    validator.check_schema(validator.schema)


def test_documents(validator: Draft, document: Document):
    validator.validate(document)
