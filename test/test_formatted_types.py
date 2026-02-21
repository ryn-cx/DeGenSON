import datetime
import ipaddress
import re
import uuid

from . import base


class TestDateTime(base.SchemaNodeTestCase):
    def test_datetime(self):
        self.add_object(datetime.datetime(2018, 11, 13, 20, 20, 39))
        self.assertResult(
            {"type": "string", "format": "date-time"}, enforceUserContract=False
        )

    def test_datetime_mixed_with_string(self):
        self.add_object(datetime.datetime(2018, 11, 13, 20, 20, 39))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "date-time"},
                ]
            },
            enforceUserContract=False,
        )


class TestDate(base.SchemaNodeTestCase):
    def test_date(self):
        self.add_object(datetime.date(2018, 11, 13))
        self.assertResult(
            {"type": "string", "format": "date"}, enforceUserContract=False
        )

    def test_date_mixed_with_string(self):
        self.add_object(datetime.date(2018, 11, 13))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "date"},
                ]
            },
            enforceUserContract=False,
        )


class TestDuration(base.SchemaNodeTestCase):
    def test_duration(self):
        self.add_object(datetime.timedelta(days=3))
        self.assertResult(
            {"type": "string", "format": "duration"}, enforceUserContract=False
        )

    def test_duration_mixed_with_string(self):
        self.add_object(datetime.timedelta(days=3))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "duration"},
                ]
            },
            enforceUserContract=False,
        )


class TestTime(base.SchemaNodeTestCase):
    def test_time(self):
        self.add_object(datetime.time(20, 20, 39))
        self.assertResult(
            {"type": "string", "format": "time"}, enforceUserContract=False
        )

    def test_time_mixed_with_string(self):
        self.add_object(datetime.time(20, 20, 39))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "time"},
                ]
            },
            enforceUserContract=False,
        )


class TestIPv4Address(base.SchemaNodeTestCase):
    def test_ipv4(self):
        self.add_object(ipaddress.IPv4Address("192.168.1.1"))
        self.assertResult(
            {"type": "string", "format": "ipv4"}, enforceUserContract=False
        )

    def test_ipv4_mixed_with_string(self):
        self.add_object(ipaddress.IPv4Address("192.168.1.1"))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "ipv4"},
                ]
            },
            enforceUserContract=False,
        )


class TestIPv6Address(base.SchemaNodeTestCase):
    def test_ipv6(self):
        self.add_object(ipaddress.IPv6Address("::1"))
        self.assertResult(
            {"type": "string", "format": "ipv6"}, enforceUserContract=False
        )

    def test_ipv6_mixed_with_string(self):
        self.add_object(ipaddress.IPv6Address("::1"))
        self.add_object("hello")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "ipv6"},
                ]
            },
            enforceUserContract=False,
        )


class TestUUID(base.SchemaNodeTestCase):
    def test_uuid(self):
        self.add_object(uuid.UUID("3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"))
        self.assertResult(
            {"type": "string", "format": "uuid"}, enforceUserContract=False
        )

    def test_uuid_mixed_with_string(self):
        self.add_object(uuid.UUID("3e4666bf-d5e5-4aa7-b8ce-cefe41c7568a"))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "uuid"},
                ]
            },
            enforceUserContract=False,
        )


class TestRegex(base.SchemaNodeTestCase):
    def test_regex(self):
        self.add_object(re.compile(r""))
        self.assertResult(
            {"type": "string", "format": "regex"}, enforceUserContract=False
        )

    def test_regex_mixed_with_string(self):
        self.add_object(re.compile(r""))
        self.add_object("test string")
        self.assertResult(
            {
                "anyOf": [
                    {"type": "string"},
                    {"type": "string", "format": "regex"},
                ]
            },
            enforceUserContract=False,
        )
