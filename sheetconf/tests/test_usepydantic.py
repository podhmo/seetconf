# type: ignore
from __future__ import annotations
import typing as t
import pydantic


class PersonConfig(pydantic.BaseModel):
    name: str


class Config(pydantic.BaseModel):
    xxx: PersonConfig
    yyy: PersonConfig
    zzz_list: t.List[PersonConfig]


def test_section_names():
    from sheetconf.usepydantic import Parser

    dummy_loader = None
    parser = Parser(Config, loader=dummy_loader)
    got = parser.section_names
    want = ["xxx", "yyy", "zzz_list"]
    assert sorted(got) == sorted(want)
