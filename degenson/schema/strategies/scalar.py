import datetime
import ipaddress
import re
import uuid

from .base import SchemaStrategy, TypedSchemaStrategy, FormattedSchemaStrategy


class Typeless(SchemaStrategy):
    """
    schema strategy for schemas with no type. This is only used when
    there is no other active strategy, and it will be merged into the
    first typed strategy that gets added.
    """

    @classmethod
    def match_schema(cls, schema):
        return "type" not in schema

    @classmethod
    def match_object(cls, obj):
        return False


class Null(TypedSchemaStrategy):
    """
    strategy for null schemas
    """

    JS_TYPE = "null"
    PYTHON_TYPE = type(None)


class Boolean(TypedSchemaStrategy):
    """
    strategy for boolean schemas
    """

    JS_TYPE = "boolean"
    PYTHON_TYPE = bool


class String(TypedSchemaStrategy):
    """
    strategy for string schemas - works for ascii and unicode strings
    """

    JS_TYPE = "string"
    PYTHON_TYPE = str


class Float(TypedSchemaStrategy):
    """
    strategy for float schemas
    """

    JS_TYPE = "number"
    PYTHON_TYPE = float


class Integer(TypedSchemaStrategy):
    """
    strategy for integer schemas
    """

    JS_TYPE = "integer"
    PYTHON_TYPE = int

    @classmethod
    def match_object(cls, obj):
        # cannot use isinstance() because boolean is a subtype of int
        return type(obj) is cls.PYTHON_TYPE


class DateTime(FormattedSchemaStrategy):
    """
    strategy for datetime.datetime schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = datetime.datetime
    FORMAT = "date-time"


class Date(FormattedSchemaStrategy):
    """
    strategy for datetime.date schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = datetime.date
    FORMAT = "date"


class Duration(FormattedSchemaStrategy):
    """
    strategy for datetime.timedelta schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = datetime.timedelta
    FORMAT = "duration"


class Time(FormattedSchemaStrategy):
    """
    strategy for datetime.time schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = datetime.time
    FORMAT = "time"


class IPv4Address(FormattedSchemaStrategy):
    """
    strategy for ipaddress.IPv4Address schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = ipaddress.IPv4Address
    FORMAT = "ipv4"


class IPv6Address(FormattedSchemaStrategy):
    """
    strategy for ipaddress.IPv6Address schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = ipaddress.IPv6Address
    FORMAT = "ipv6"


class UUID(FormattedSchemaStrategy):
    """
    strategy for uuid.UUID schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = uuid.UUID
    FORMAT = "uuid"


class Regex(FormattedSchemaStrategy):
    """
    strategy for re.Pattern schemas

    Not JSON compliant.
    """

    JS_TYPE = "string"
    PYTHON_TYPE = re.Pattern
    FORMAT = "regex"
