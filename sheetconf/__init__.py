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


class CSVFileAccessor:
    def __init__(self) -> None:
        import csv

        self._reader_class = csv.DictReader

    def fetch_rows(self, filename: t.Union[str, pathlib.Path]) -> t.Iterator[RowDict]:
        with open(filename) as rf:
            reader = self._reader_class(rf)  # DictReader?
            for line in reader:
                row = t.cast(RowDict, line)  # xxx
                if "value_type" not in row:
                    row["value_type"] = "str"  # xxx
                if "description" not in row:
                    row["description"] = None
                yield row

    def store_rows(
        self, filename: t.Union[str, pathlib.Path, None], rows: t.Iterator[RowDict]
    ) -> None:
        import csv
        import contextlib

        with contextlib.ExitStack() as s:
            wf = sys.stdout
            if filename is not None:
                wf = s.enter_context(open(filename, "w"))

            w = csv.DictWriter(
                wf, fieldnames=["name", "value", "value_type", "description"]
            )
            w.writeheader()
            w.writerows(rows)


class CSVLoader:
    def __init__(self, *, ext: str = ".csv") -> None:
        self.ext = ext

    def _get_filepath(
        self, basedir: t.Optional[str], section_name: str
    ) -> pathlib.Path:
        basepath = pathlib.Path(basedir or ".")
        return (basepath / section_name).with_suffix(self.ext)

    def load(
        self, basedir: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        accessor = CSVFileAccessor()

        def _get_rows(section_name: str) -> t.Iterator[RowDict]:
            filepath = self._get_filepath(basedir, section_name)
            try:
                rows = accessor.fetch_rows(filepath)
                return iter(list(rows))  # for detecting FileNotFoundError here
            except FileNotFoundError:
                return iter([])

        return Extractor(introspector).extract_config_data(get_rows=_get_rows)

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        basedir: t.Optional[str] = None,
        *,
        introspector: Introspector,
    ) -> None:
        ob = ob or {}
        accessor = CSVFileAccessor()
        extractor = Extractor(introspector)
        if basedir is not None and not pathlib.Path(basedir).exists():
            pathlib.Path(basedir).mkdir(parents=True)

        for section in introspector.section_names:
            rows = extractor.extract_rows_with_config_data(ob, section)

            csvpath: t.Optional[pathlib.Path] = self._get_filepath(basedir, section)
            if basedir is None:
                print(f"* file {csvpath}", file=sys.stderr)
                csvpath = None
            accessor.store_rows(csvpath, rows)


class Extractor:
    def __init__(self, introspector: Introspector) -> None:
        self.introspector = introspector
        self._get_translate_function = get_translate_function

    def extract_config_data(
        self, *, get_rows: t.Callable[[str], t.Iterator[RowDict]]
    ) -> t.Dict[str, t.Any]:
        data: t.Dict[str, t.Any] = {}
        introspector = self.introspector
        for section in introspector.section_names:
            rows = get_rows(section)
            section_data = {}
            for row in rows:
                _translate = self._get_translate_function(row["value_type"])
                section_data[row["name"]] = _translate(row["value"])
            data[section] = section_data
        return data

    def extract_rows_with_config_data(
        self, ob: t.Dict[str, t.Any], section: str
    ) -> t.Iterator[RowDict]:
        sob = ob.get(section) or {}

        for row in self.introspector.get_fields(section):
            if row["name"] in sob:
                row["value"] = sob[row["name"]]
            yield row


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
