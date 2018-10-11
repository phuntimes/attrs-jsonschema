#!/usr/bin/env python
# -*- coding: utf-8 -*-

import attr
import typing

from attr import Attribute
from typing import Any, Mapping, Callable, NoReturn
from jsonschema import validate, ValidationError, SchemaError


Schema = Mapping[str, Any]
Validator = Callable[[Any, Attribute, Any], NoReturn]


is_dict = attr.validators.instance_of(dict)


@attr.s(frozen=True, slots=True)
class JSONValidator(Validator):
    """
    A basic :class:`Attribute` validator utilizing a JSON schema.
    Since basic functionality utilizes :func:`validate`:

     - schema is not validated until callback
     - only the first encountered error is reported

    Wherein schema draft utilized is determined from:

     - `$schema` property in schema
     - or, if not present, most recent draft
    """

    schema: Schema = attr.ib(validator=is_dict)

    def __call__(self, i: Any, a: Attribute, v: Any):
        """
        Validate that passed document lints against schema.

        :param i: dataclass instance
        :param a: attribute instance
        :param v: passed value
        :raises ValueError: if fails linting
        """
        m = "'{:s}' failed linting against {:s}"

        try:
            validate(v, self.schema)

        except SchemaError as e:
            m = m.format(a.name, 'metaschema')
            raise ValueError(m, a, v) from e

        except ValidationError as e:
            m = m.format(a.name, 'schema')
            raise ValueError(m, a, v) from e

