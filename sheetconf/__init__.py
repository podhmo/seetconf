from __future__ import annotations
import typing as t
import logging

logger = logging.getLogger(__name__)
if t.TYPE_CHECKING:
    from sheetconf.types import Loader, Parser, ConfigT, RowDict

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


class RowsLoader:
    def __init__(self, get_rows: t.Callable[[str, str], t.Iterator[RowDict]]) -> None:
        self._get_rows_function = get_rows
        self._translate_functions = {
            "float": float,
            "int": int,
            "str": str,
        }  # todo: refinement

    def load(self, filename: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        data: t.Dict[str, t.Any] = {}
        for section in parser.section_names:
            rows = self._get_rows_function(filename, section)
            section_data = {}
            for row in rows:
                _translate = self._translate_functions.get(row["value_type"], str)
                section_data[row["name"]] = _translate(row["value"])
            data[section] = section_data
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
