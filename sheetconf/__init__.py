from __future__ import annotations
import typing as t
import typing_extensions as tx

# TODO
# - todo: validation
# - todo: load csv files
# - todo: load spreadsheet
# - todo: add cli
# - todo: support default value
# - todo: support sections (as default)
# - todo: support list
# - todo: support nested dict


class Loader(tx.Protocol):
    def load(self, source: str) -> t.Dict[str, t.Any]:
        ...


class Fetcher(tx.Protocol):
    def fetch(self, url: str) -> t.Dict[str, t.Any]:
        ...


class JSONLoader:
    def __init__(self, *, params: t.Optional[t.Dict[str, t.Any]] = None) -> None:
        self.params = params or {}

    def load(self, filename: str) -> t.Dict[str, t.Any]:
        import json

        with open(filename) as rf:
            return json.load(rf)
