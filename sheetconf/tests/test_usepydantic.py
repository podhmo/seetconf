# type: ignore
from __future__ import annotations
import typing as t
import pydantic


class PersonConfig(pydantic.BaseModel):
    name: str = pydantic.Field(description="name of person")
    age: int = pydantic.Field(default=0)
    nickname: t.Optional[str]


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
        {
            "name": "name",
            "value": None,
            "value_type": "str",
            "description": "name of person",
        },
        {"name": "age", "value": 0, "value_type": "int", "description": None},
        {"name": "nickname", "value": None, "value_type": "str", "description": None},
    ]
    assert got == want
