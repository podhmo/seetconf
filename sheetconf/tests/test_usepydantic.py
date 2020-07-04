# type: ignore
from __future__ import annotations
import typing as t
import pydantic


class PersonConfig(pydantic.BaseModel):
    name: str
    age: int


class Config(pydantic.BaseModel):
    xxx: PersonConfig
    yyy: PersonConfig
    zzz_list: t.List[PersonConfig]


def test_section_names():
    from sheetconf.usepydantic import Introspector

    introspector = Introspector(Config)
    got = introspector.section_names
    want = ["xxx", "yyy", "zzz_list"]
    assert sorted(got) == sorted(want)


def test_get_fields():
    from sheetconf.usepydantic import Introspector

    introspector = Introspector(Config)
    got = list(introspector.get_fields("xxx"))
    want = [
        {"name": "name", "value": None, "value_type": "str", "description": None},
        {"name": "age", "value": None, "value_type": "int", "description": None},
    ]
    assert got == want
