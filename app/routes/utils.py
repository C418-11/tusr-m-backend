# -*- coding: utf-8 -*-


import mimetypes
from typing import Any
from typing import Mapping
from typing import cast

from flask import request
from marshmallow import Schema
from marshmallow import ValidationError
from werkzeug.exceptions import UnsupportedMediaType

from ..api import APIArgumentError
from ..api import APIException

type JSONLike = Mapping[str, Any]


def validate_json_arguments(schema: type[Schema], optional: bool = False) -> JSONLike:
    try:
        return schema().load(cast(JSONLike, request.json), unknown="raise")  # type: ignore[no-any-return]
    except ValidationError as err:
        raise APIException(APIArgumentError(arguments=err.messages))
    except UnsupportedMediaType as err:
        if not optional:
            raise
        if mimetypes.types_map[".json"] not in err.description:
            raise
        return {}


__all__ = (
    "JSONLike",
    "validate_json_arguments",
)
