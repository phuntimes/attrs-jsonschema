#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import attr

from attr import Attribute
from typing import Any
from jsonschema import ValidationError

from .basic import JSONValidator
from .schema import SchemaValidator

from .pep484 import Schema, Drafts, Draft3, Draft4


@attr.s(frozen=True, slots=True)
class DraftXValidator(JSONValidator):
    """
    Class for explicitly validating schema against draft.
    Advantages of this are:

     - (one-time) schema validation against specified draft
     - collate all schema violations for error reporting
    """

    validator: Drafts = attr.ib(init=False, repr=False)

    @abc.abstractmethod
    def __attrs_post_init__(self):
        pass

    def __call__(self, i: Any, a: Attribute, v: Any):
        """
        Validate that passed document lints against schema.

        :param i: dataclass instance
        :param a: attribute instance
        :param v: passed value
        :raises ValueError: if fails linting
        """
        # TODO ErrorTree
        try:
            self.validator.validate(v)
        except ValidationError as e:
            m = "'{:s}' failed linting against schema"
            raise ValidationError(m.format(a.name)) from e


is_draft3 = SchemaValidator(Draft3)
is_draft4 = SchemaValidator(Draft4)


@attr.s(frozen=True, slots=True)
class Draft4Validator(DraftXValidator):

    schema: Schema = attr.ib(validator=is_draft4)
    validator: Draft4 = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        new = Draft4(self.schema)
        object.__setattr__(self, 'validator', new)


@attr.s(frozen=True, slots=True)
class Draft3Validator(DraftXValidator):

    schema: Schema = attr.ib(validator=is_draft3)
    validator: Draft3 = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        new = Draft3(self.schema)
        object.__setattr__(self, 'validator', new)
