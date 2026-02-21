from .base import SchemaStrategy, TypedSchemaStrategy
from .scalar import (
    Typeless,
    Null,
    Boolean,
    Float,
    Integer,
    String,
)
from .array import List, Tuple
from .object import Object

BASIC_SCHEMA_STRATEGIES = (
    Null,
    Boolean,
    Float,
    Integer,
    String,
    List,
    Tuple,
    Object,
)

__all__ = (
    "SchemaStrategy",
    "TypedSchemaStrategy",
    "Null",
    "Boolean",
    "Float",
    "Integer",
    "String",
    "List",
    "Tuple",
    "Object",
    "Typeless",
    "BASIC_SCHEMA_STRATEGIES",
)
