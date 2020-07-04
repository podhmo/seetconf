from __future__ import annotations
import typing as t

if t.TYPE_CHECKING:
    from sheetconf.types import Loader, Parser, ConfigT

# TODO
# - todo: validation
# - todo: load csv files
# - todo: load spreadsheet
# - todo: add cli
# - todo: support default value
# - todo: support sections (as default)
# - todo: support list
# - todo: support nested dict


class JSONLoader:
    def __init__(self, params: t.Optional[t.Dict[str, t.Any]] = None) -> None:
        self.params = params or {}

    def load(self, filename: str) -> t.Dict[str, t.Any]:
        import json

        with open(filename) as rf:
            return json.load(rf)


def load(filename: str, *, parser: Parser[ConfigT]) -> ConfigT:
    return parser.parse(filename)
