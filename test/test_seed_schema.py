import uuid

from . import base


class TestSeedTuple(base.SchemaNodeTestCase):
    def test_tuple(self):
        self.add_schema({"type": "array", "items": []})
        self.add_object([None])
        self.assertResult({"type": "array", "items": [{"type": "null"}]})


class TestUUIDProperties(base.SchemaNodeTestCase):
    def test_seeded_format_round_trips(self):
        self.add_schema({"type": "string", "format": "uuid"})
        self.assertResult({"type": "string", "format": "uuid"})

    def test_seeded_format_widens_with_plain_string(self):
        self.add_schema({"type": "string", "format": "uuid"})
        self.add_object("77db3944-8426-4259-94c8-be147d3e7594::1")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "uuid"},
                ]
            }
        )

    def test_seeded_format_widens_with_matching_object(self):
        self.add_schema({"type": "string", "format": "uuid"})
        self.add_object(uuid.UUID("77db3944-8426-4259-94c8-be147d3e7594"))
        self.assertResult(
            {"type": "string", "format": "uuid"}, enforceUserContract=False
        )

    def test_seeded_union_round_trips(self):
        self.add_schema(
            {"anyOf": [{"type": "string"}, {"type": "string", "format": "uuid"}]}
        )
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "uuid"},
                ]
            }
        )

    def test_seeded_unknown_format_falls_back_to_string(self):
        self.add_schema({"type": "string", "format": "email"})
        self.assertResult({"type": "string", "format": "email"})


class TestPatternProperties(base.SchemaNodeTestCase):
    def test_single_pattern(self):
        self.add_schema({"type": "object", "patternProperties": {r"^\d$": None}})
        self.add_object({"0": 0, "1": 1, "2": 2})
        self.assertResult(
            {"type": "object", "patternProperties": {r"^\d$": {"type": "integer"}}}
        )

    def test_multi_pattern(self):
        self.add_schema(
            {"type": "object", "patternProperties": {r"^\d$": None, r"^[a-z]$": None}}
        )
        self.add_object({"0": 0, "1": 1, "a": True, "b": False})
        self.assertResult(
            {
                "type": "object",
                "patternProperties": {
                    r"^\d$": {"type": "integer"},
                    r"^[a-z]$": {"type": "boolean"},
                },
            }
        )

    def test_multi_pattern_multi_object(self):
        self.add_schema(
            {"type": "object", "patternProperties": {r"^\d$": None, r"^[a-z]$": None}}
        )
        self.add_object({"0": 0})
        self.add_object({"1": 1})
        self.add_object({"a": True})
        self.add_object({"b": False})
        self.assertResult(
            {
                "type": "object",
                "patternProperties": {
                    r"^\d$": {"type": "integer"},
                    r"^[a-z]$": {"type": "boolean"},
                },
            }
        )

    def test_existing_schema(self):
        self.add_schema(
            {"type": "object", "patternProperties": {r"^\d$": {"type": "boolean"}}}
        )
        self.add_object({"0": 0, "1": 1, "2": 2})
        self.assertResult(
            {
                "type": "object",
                "patternProperties": {r"^\d$": {"type": ["boolean", "integer"]}},
            }
        )

    def test_prefers_existing_properties(self):
        self.add_schema(
            {
                "type": "object",
                "properties": {"0": None},
                "patternProperties": {r"^\d$": None},
            }
        )
        self.add_object({"0": 0, "1": 1, "2": 2})
        self.assertResult(
            {
                "type": "object",
                "properties": {"0": {"type": "integer"}},
                "patternProperties": {r"^\d$": {"type": "integer"}},
                "required": ["0"],
            }
        )

    def test_keeps_unrecognized_properties(self):
        self.add_schema({"type": "object", "patternProperties": {r"^\d$": None}})
        self.add_object({"0": 0, "1": 1, "2": 2, "a": True})
        self.assertResult(
            {
                "type": "object",
                "properties": {"a": {"type": "boolean"}},
                "patternProperties": {r"^\d$": {"type": "integer"}},
                "required": ["a"],
            }
        )
