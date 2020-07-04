from __future__ import annotations
import typing as t
import logging

from sheetconf.types import RowDict

if t.TYPE_CHECKING:
    from sheetconf.types import Loader, Parser, ConfigT

logger = logging.getLogger(__name__)


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


class CSVLoader:
    def __init__(self, *, ext: str = ".csv") -> None:
        # todo: reify
        import csv

        self.ext = ext
        self._reader_class = csv.DictReader
        self._loader = RowsLoader(self.get_rows)

    def get_rows(self, filename: str, section_name: str) -> t.Iterator[RowDict]:
        import pathlib

        basedir = pathlib.Path(filename or ".")
        with open((basedir / section_name).with_suffix(self.ext)) as rf:
            reader = self._reader_class(rf)  # DictReader?
            for line in reader:
                row = t.cast(RowDict, line)  # xxx
                if "value_type" not in row:
                    row["value_type"] = "str"  # xxx
                if "description" not in row:
                    row["description"] = None
                yield row

    def load(self, basedir: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        return self._loader.load(basedir, parser=parser)


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
    def __init__(
        self, loader: Loader, *, section_names: t.Optional[t.List[str]] = None
    ) -> None:
        self.loader = loader
        self._section_names = section_names

    @property
    def section_names(self) -> t.List[str]:
        if self._section_names is None:
            logger.warning("not support section_names, return []")
            return []
        return self._section_names

    def parse(self, filename: str) -> t.Dict[str, t.Any]:
        return self.loader.load(filename, parser=self)


def load(filename: str, *, parser: Parser[ConfigT]) -> ConfigT:
    return parser.parse(filename)
