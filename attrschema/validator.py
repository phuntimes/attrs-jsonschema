#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import attr

from attr import Attribute
from typing import Any, Union, Type, Pattern
from jsonschema import Draft4Validator, Draft3Validator
from jsonschema import ValidationError, SchemaError

from .validate import Validator, Schema


Draft = Union[Draft4Validator, Draft3Validator]
DraftType = Type[Draft]

DRAFTS = (Draft4Validator, Draft3Validator)

DRAFT = re.compile(r'http://json-schema.org/draft-(\d+)/schema#')


def schema_version(schema: Schema, pattern: Pattern[str] = DRAFT) -> int:
    """
    Determine the schema version by regex-ing '$schema' property
    of the schema (if it exists). For example:

    {
        ...
        '$schema': 'http://json-schema.org/draft-04/schema#'
        ...
    }

    should return version `4`.

    :param schema: schema instance
    :param pattern: regex pattern to utilize
    :return: schema version
    :raises KeyError: if '$schema' property does not exist
    :raises ValueError: if '$schema' property fails search
    """

    try:
        m = pattern.search(schema['$schema'])
    except KeyError:
        raise KeyError("schema has no '$schema' property")

    if m is None:
        raise ValueError("'$schema' property failed regex")

    return int(m.group(1))


def is_draft(i: Any, a: Attribute, v: Any):
    """
    Verify that passed value is both:

     - instance of a `Validator`
     - contains a valid schema

    :param a: attribute instance
    :param v: passed value
    :raises TypeError: if not an instance
    :raises ValueError: if fails linting
    """

    if not isinstance(v, DRAFTS):
        m = "'{name:s}' is not a Validator " \
            "(is {value:!r} of type {actual:!r})".format(
                name=a.name,
                value=v,
                actual=type(v)
            )
        raise TypeError(m, a, v)

    try:
        v.check_schema(v.schema)
    except SchemaError as e:
        m = "'{name:s}' internal schema is failed linting " \
            "(expected valid draft {version:d} schema)".format(
                name=a.name,
                version=schema_version(v.schema)
            )
        raise ValueError(m, a, v.schema) from e


@attr.s(frozen=True, slots=True)
class DraftValidator(Validator):
    """
    Class for explicitly validating schema against draft.
    Advantages of this are:

     - (one-time) schema validation against specified draft
     - collate all schema violations for error reporting
    """

    validator: Draft = attr.ib(validator=is_draft, repr=False)
    schema: Schema = attr.ib(init=False)  # NOTE for repr(...)

    def __attrs_post_init__(self):
        schema = self.validator.schema
        object.__setattr__(self, 'schema', schema)

    def __call__(self, i: Any, a: Attribute, v: Any):
        """
        Validate that passed document lints against schema.

        :param i: dataclass instance
        :param a: attribute instance
        :param v: passed value
        :raises ValueError: if fails linting
        """
        # TODO ErrorTree ?
        try:
            self.validator.validate(v)
        except ValidationError as e:
            m = "'{name:s}' failed linting against schema".format(
                name=a.name
            )
            raise ValueError(m) from e
