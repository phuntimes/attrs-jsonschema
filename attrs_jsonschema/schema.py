#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr

from attr import Attribute
from typing import Any
from jsonschema import SchemaError

from .generics import Validator, Drafts, DraftTypes
from .version import schema_version


def is_type(i: Any, a: Attribute, v: Any):
    """
    Validate that passed value is a validator type.

    :param i: dataclass instance
    :param a: attribute instance
    :param v: passed value
    :raises TypeError: if not validator type
    """
    if not issubclass(v, Drafts.__args__):
        m = "'{:s}' must be an 'IValidator'; got {!r}"
        raise TypeError(m.format(a.name, type(v)))


@attr.s(slots=True, frozen=True)
class SchemaValidator(Validator):
    """
    A :class:`Attribute` validator for validating a JSON schema explicitly
    against a specified draft version. Utilized in specific :class:`Attribute`
    validators which specify draft version.
    """

    draft: DraftTypes = attr.ib(validator=is_type)
    version: int = attr.ib(init=False)

    def __attrs_post_init__(self):
        v = schema_version(self.draft.META_SCHEMA)
        object.__setattr__(self, 'version', v)

    def __call__(self, i: Any, a: Attribute, v: Any):
        """
        Validate that passed schema lints against draft schema.

        :param i: dataclass instance
        :param a: attribute instance
        :param v: passed value
        :raises SchemaError: if fails linting
        """
        try:
            self.draft.check_schema(v)
        except SchemaError as e:
            m = "'{:s}' failed linting against schema draft v{:d}"
            raise SchemaError(m.format(a.name, self.version)) from e

