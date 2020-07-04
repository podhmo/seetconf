from __future__ import annotations
import typing as t
import sys
import pathlib
import logging

from sheetconf.types import RowDict
from sheetconf import exceptions

if t.TYPE_CHECKING:
    from sheetconf.types import Loader, Fetcher, Parser, ConfigT

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

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        filename: t.Optional[str] = None,
        *,
        parser: Parser[t.Any],
    ) -> None:
        ob = ob or {}
        d = {}
        for section in parser.section_names:
            sob = ob.get(section) or {}
            d[section] = {
                row["name"]: sob.get(row["name"]) or row["value"]
                for row in parser.get_fields(section)
            }

        import json
        import contextlib

        with contextlib.ExitStack() as s:
            wf = sys.stdout
            if filename is not None:
                wf = s.enter_context(open(filename))
            json.dump(d, wf, indent=2, ensure_ascii=False)
            print(file=wf)


class CSVFetcher:
    def __init__(self) -> None:
        import csv

        self._reader_class = csv.DictReader

    def fetch(self, filename: str) -> t.Iterator[RowDict]:
        with open(filename) as rf:
            reader = self._reader_class(rf)  # DictReader?
            for line in reader:
                row = t.cast(RowDict, line)  # xxx
                if "value_type" not in row:
                    row["value_type"] = "str"  # xxx
                if "description" not in row:
                    row["description"] = None
                yield row


class CSVLoader:
    def __init__(self, *, ext: str = ".csv") -> None:
        self.ext = ext
        self._fetcher: Fetcher = CSVFetcher()
        self._loader = RowsLoader(self._get_rows)

    def _get_rows(self, basedir: str, section_name: str) -> t.Iterator[RowDict]:
        filepath = self._get_filepath(basedir, section_name)
        return self._fetcher.fetch(str(filepath))

    def _get_filepath(
        self, basedir: t.Optional[str], section_name: str
    ) -> pathlib.Path:
        basepath = pathlib.Path(basedir or ".")
        return (basepath / section_name).with_suffix(self.ext)

    def load(self, filename: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        return self._loader.load(filename, parser=parser)

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        basedir: t.Optional[str] = None,
        *,
        parser: Parser[t.Any],
    ) -> None:
        import csv
        import contextlib

        ob = ob or {}
        for section in parser.section_names:
            rows = []
            sob = ob.get(section) or {}

            for row in parser.get_fields(section):
                if row["name"] in sob:
                    row["value"] = sob[row["name"]]
                rows.append(row)

            with contextlib.ExitStack() as s:
                wf = sys.stdout
                csvpath = self._get_filepath(basedir, section)

                if basedir is not None:
                    wf = s.enter_context(open(csvpath))

                if wf == sys.stdout:
                    print(f"* file {csvpath}", file=sys.stderr)

                w = csv.DictWriter(
                    wf, fieldnames=["name", "value", "value_type", "description"]
                )
                w.writeheader()
                w.writerows(rows)


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


def loadfile(filename: str, *, parser: Parser[ConfigT]) -> ConfigT:
    try:
        return parser.parse(filename)
    except exceptions.CredentialsFileIsNotFound as e:
        print(repr(e), file=sys.stderr)
        print(
            f"""\tPlease save file at {e} (OAuth 2.0 client ID)""", file=sys.stderr,
        )
        import webbrowser

        url = "https://console.cloud.google.com/apis/credentials"
        print(f"\topening... {url}", file=sys.stderr)
        webbrowser.open(url, new=1, autoraise=True)
        raise


def savefile(
    ob: t.Any, filename: t.Optional[str] = None, *, parser: Parser[ConfigT]
) -> None:
    parser.unparse(ob, filename)
