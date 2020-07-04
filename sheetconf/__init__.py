from __future__ import annotations
import typing as t
import logging

logger = logging.getLogger(__name__)
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

    def load(self, filename: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        import json

        with open(filename) as rf:
            data: t.Dict[str, t.Any] = json.load(rf)
        return data


class RawParser:
    def __init__(self, loader: Loader) -> None:
        self.loader = loader

    @property
    def section_names(self) -> t.List[str]:
        logger.warning("not support section_names, return []")
        return []

    def parse(self, filename: str) -> t.Dict[str, t.Any]:
        return self.loader.load(filename, parser=self)


def load(filename: str, *, parser: Parser[ConfigT]) -> ConfigT:
    return parser.parse(filename)
