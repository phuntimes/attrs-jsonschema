#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from jsonschema import Draft4Validator as Draft4

from tests.fixtures import JSONObject


@pytest.fixture
def geojson_validator(geojson_schema: JSONObject) -> Draft4:
    return Draft4(geojson_schema)


def test_schema_against_draft_4(
        geojson_schema: JSONObject
):
    Draft4.check_schema(geojson_schema)


def test_samples_against_schema(
        geojson_validator: Draft4,
        geojson_samples: JSONObject
):
    geojson_validator.validate(geojson_samples)
