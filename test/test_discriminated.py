from degenson import discriminated_builder
from . import base


class DiscriminatedBuilderTestCase(base.SchemaNodeTestCase):
    def setUp(self):
        self.builder = discriminated_builder("type")
        self._objects = []
        self._schemas = []


class TestAddObject(DiscriminatedBuilderTestCase):
    def test_single_variant(self):
        self.add_object({"type": "cat", "meow": True})
        self.assertResult(
            {
                "$schema": "http://json-schema.org/schema#",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "cat"},
                            "meow": {"type": "boolean"},
                        },
                        "required": ["meow", "type"],
                        "title": "cat",
                    },
                ],
                "discriminator": {"propertyName": "type"},
            }
        )

    def test_multiple_variants(self):
        self.add_object({"type": "cat", "meow": True})
        self.add_object({"type": "dog", "bark": 5})
        self.assertResult(
            {
                "$schema": "http://json-schema.org/schema#",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "cat"},
                            "meow": {"type": "boolean"},
                        },
                        "required": ["meow", "type"],
                        "title": "cat",
                    },
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "dog"},
                            "bark": {"type": "integer"},
                        },
                        "required": ["bark", "type"],
                        "title": "dog",
                    },
                ],
                "discriminator": {"propertyName": "type"},
            }
        )

    def test_variants_merge_by_discriminator(self):
        self.add_object({"type": "cat", "meow": True})
        self.add_object({"type": "cat", "meow": False, "lives": 9})
        self.assertResult(
            {
                "$schema": "http://json-schema.org/schema#",
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "cat"},
                            "meow": {"type": "boolean"},
                            "lives": {"type": "integer"},
                        },
                        "required": ["meow", "type"],
                        "title": "cat",
                    },
                ],
                "discriminator": {"propertyName": "type"},
            }
        )

    def test_variants_sorted_by_value(self):
        self.add_object({"type": "dog", "bark": 5})
        self.add_object({"type": "cat", "meow": True})
        titles = [variant["title"] for variant in self.builder.to_schema()["oneOf"]]
        self.assertEqual(["cat", "dog"], titles)


class TestAddSchema(DiscriminatedBuilderTestCase):
    def test_roundtrip(self):
        source = discriminated_builder("type")
        source.add_object({"type": "cat", "meow": True})
        source.add_object({"type": "dog", "bark": 5})
        expected = source.to_schema()

        self.add_schema(expected)
        self.assertResult(expected)

    def test_object_merges_into_schema_variant(self):
        self.add_schema(
            {
                "oneOf": [
                    {
                        "type": "object",
                        "properties": {
                            "type": {"const": "cat"},
                            "meow": {"type": "boolean"},
                        },
                        "required": ["meow", "type"],
                    }
                ],
                "discriminator": {"propertyName": "type"},
            }
        )
        self.add_object({"type": "cat", "purr": True})
        result = self.builder.to_schema()
        variant = result["oneOf"][0] if "oneOf" in result else result
        self.assertEqual(
            {
                "type": {"const": "cat"},
                "meow": {"type": "boolean"},
                "purr": {"type": "boolean"},
            },
            variant["properties"],
        )
        self.assertEqual(["type"], variant["required"])
