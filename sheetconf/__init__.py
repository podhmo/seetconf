from __future__ import annotations
import typing as t
import typing_extensions as tx
import sys
import pathlib
import logging

from sheetconf.types import RowDict
from sheetconf.langhelpers import get_translate_function
from sheetconf import exceptions

if t.TYPE_CHECKING:
    from sheetconf.types import Loader, Parser, Introspector, ConfigT

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

    def load(
        self, filename: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        import json

        with open(filename) as rf:
            data: t.Dict[str, t.Any] = json.load(rf)
        return data

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        filename: t.Optional[str] = None,
        *,
        introspector: Introspector,
    ) -> None:
        ob = ob or {}
        d = {}
        for section in introspector.section_names:
            sob = ob.get(section) or {}
            d[section] = {
                row["name"]: sob.get(row["name"]) or row["value"]
                for row in introspector.get_fields(section)
            }

        import json
        import contextlib

        with contextlib.ExitStack() as s:
            wf = sys.stdout
            if filename is not None:
                wf = s.enter_context(open(filename, "w"))
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
        self._fetcher = CSVFetcher()
        self._loader = RowsLoader(self._get_rows)

    def _get_rows(self, basedir: str, section_name: str) -> t.Iterator[RowDict]:
        filepath = self._get_filepath(basedir, section_name)
        try:
            rows = self._fetcher.fetch(str(filepath))
            return iter(list(rows))  # for detecting FileNotFoundError here
        except FileNotFoundError:
            return iter([])

    def _get_filepath(
        self, basedir: t.Optional[str], section_name: str
    ) -> pathlib.Path:
        basepath = pathlib.Path(basedir or ".")
        return (basepath / section_name).with_suffix(self.ext)

    def load(
        self, filename: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        return self._loader.load(filename, introspector=introspector, adjust=adjust)

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        basedir: t.Optional[str] = None,
        *,
        introspector: Introspector,
    ) -> None:
        import csv
        import contextlib

        ob = ob or {}
        if basedir is not None and not pathlib.Path(basedir).exists():
            pathlib.Path(basedir).mkdir(parents=True)

        # todo: refactoring
        for section in introspector.section_names:
            rows = []
            sob = ob.get(section) or {}

            for row in introspector.get_fields(section):
                if row["name"] in sob:
                    row["value"] = sob[row["name"]]
                rows.append(row)

            with contextlib.ExitStack() as s:
                wf = sys.stdout
                csvpath = self._get_filepath(basedir, section)

                if basedir is not None:
                    wf = s.enter_context(open(csvpath, "w"))

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
        self._get_translate_function = get_translate_function

    def load(
        self, filename: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        data: t.Dict[str, t.Any] = {}
        for section in introspector.section_names:
            rows = self._get_rows_function(filename, section)
            section_data = {}
            for row in rows:
                _translate = self._get_translate_function(row["value_type"])
                section_data[row["name"]] = _translate(row["value"])
            data[section] = section_data
        return data


def loadfile(
    filename: str, *, parser: Parser[ConfigT], adjust: bool = False
) -> ConfigT:
    try:
        return parser.parse(filename, adjust=adjust)
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


def get_loader(*, format: tx.Literal["json", "csv", "spreadsheet"]) -> Loader:
    if format == "json":
        return JSONLoader()
    elif format == "csv":
        return CSVLoader(ext=".csv")
    elif format == "spreadsheet":
        from sheetconf.usegspread import Loader as GspreadLoader

        return GspreadLoader()
    else:
        raise exceptions.UnsupportedFormat(format)
