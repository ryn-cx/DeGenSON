from .base import SchemaStrategy
from .object import Object


class DiscriminatedObject(SchemaStrategy):
    """
    abstract discriminated object schema strategy
    """

    DISCRIMINATOR_KEY = None
    KEYWORDS = ("type", "oneOf", "discriminator")

    @classmethod
    def match_object(cls, obj):
        return (
            cls.DISCRIMINATOR_KEY is not None
            and isinstance(obj, dict)
            and cls.DISCRIMINATOR_KEY in obj
        )

    @classmethod
    def match_schema(cls, schema):
        discriminator = schema.get("discriminator")
        return (
            isinstance(discriminator, dict)
            and discriminator.get("propertyName") == cls.DISCRIMINATOR_KEY
        )

    def __init__(self, node_class):
        super().__init__(node_class)
        self._variants = {}

    def _variant(self, value):
        strategy = self._variants.get(value)
        if strategy is None:
            strategy = Object(self.node_class)
            self._variants[value] = strategy
        return strategy

    def add_object(self, obj):
        self._variant(obj[self.DISCRIMINATOR_KEY]).add_object(obj)

    def add_schema(self, schema):
        super().add_schema(schema)
        variants = schema.get("oneOf", [schema] if "properties" in schema else [])
        for variant in variants:
            marker = variant.get("properties", {}).get(self.DISCRIMINATOR_KEY, {})
            self._variant(marker.get("const")).add_schema(variant)

    def to_schema(self):
        variants = []
        for value in sorted(self._variants, key=str):
            variant = self._variants[value].to_schema()
            properties = variant.setdefault("properties", {})
            properties[self.DISCRIMINATOR_KEY] = {"const": value}
            required = set(variant.get("required", ()))
            required.add(self.DISCRIMINATOR_KEY)
            variant["required"] = sorted(required)
            variant["title"] = str(value)
            variants.append(variant)

        if len(variants) == 1:
            schema = variants[0]
        else:
            schema = {
                "oneOf": variants,
                "discriminator": {"propertyName": self.DISCRIMINATOR_KEY},
            }
        schema.update(self._extra_keywords)
        return schema
