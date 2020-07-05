from __future__ import annotations
import typing as t
import typing_extensions as tx
import pathlib
from sheetconf import Extractor
from sheetconf.types import RowDict
from sheetconf.langhelpers import reify
from sheetconf import exceptions

if t.TYPE_CHECKING:
    from sheetconf.types import Introspector
    from gspread.client import Client
    from gspread.models import Spreadsheet, Worksheet


class Accessor:
    def __init__(self, sheet: Spreadsheet) -> None:
        self.sheet = sheet

    @reify
    def worksheet_mapping(self) -> t.Dict[str, Worksheet]:
        return {ws.title: ws for ws in self.sheet.worksheets()}

    def fetch_rows(self, sheet_title: str) -> t.Iterator[RowDict]:
        if sheet_title not in self.worksheet_mapping:
            # TODO: logging
            return []

        ws = self.sheet.worksheet(sheet_title)
        for row in ws.get("A1:E"):
            name = row[0]
            value = row[1]
            value_type: tx.Literal["str", "float", "int"] = "str"
            description = None

            if len(row) >= 3:
                value_type = row[2]
            if len(row) >= 4:
                description = row[3]
            row_dict: RowDict = {
                "name": name,
                "value": value,
                "value_type": value_type,
                "description": description,
            }
            yield row_dict

    def store_rows(self, _rows: t.Iterator[RowDict], sheet_title: str) -> None:
        rows = list(_rows)
        ws = self.worksheet_mapping.get(sheet_title)
        if ws is None:
            ws = self.worksheet_mapping[sheet_title] = self.sheet.add_worksheet(
                title=sheet_title, cols="4", rows=str(len(rows) + 1)
            )
        values = [["name", "value", "value_type", "description"]]
        for row in rows:
            values.append(
                [
                    row["name"],
                    str(row["value"]),
                    row["value_type"],
                    row["description"] or "",
                ]
            )
        ws.update(f"A1:E{len(rows)+1}", values)


class Loader:
    def __init__(
        self,
        *,
        scopes: t.Optional[t.List[str]] = None,
        credential_file: str = "~/.config/sheetconf/credentials.json",
        authorized_user_filename: str = "~/.config/sheetconf/authorized_user.json",
        port: int = 0,
    ) -> None:
        from gspread.auth import DEFAULT_SCOPES

        self.scopes = scopes or DEFAULT_SCOPES
        self.credential_filename = credential_file
        self.authorized_user_filename = authorized_user_filename
        self.port = port
        self._accessors: t.Dict[str, Accessor] = {}  # weakref?

    def _get_accessor(self, sheet_url: str) -> Accessor:
        accessor = self._accessors.get(sheet_url)
        if accessor is None:
            sheet = self.client.open_by_url(sheet_url)
            accessor = self._accessors[sheet_url] = Accessor(sheet)
        return accessor

    def load(
        self, sheet_url: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        def _get_rows(section_name: str) -> t.Iterator[RowDict]:
            accessor = self._get_accessor(sheet_url)
            return accessor.fetch_rows(section_name)

        return Extractor(introspector).extract_config_data(get_rows=_get_rows)

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        sheet_url: t.Optional[str] = None,
        *,
        introspector: Introspector,
    ) -> None:
        if sheet_url is None:
            raise RuntimeError("need sheet-url")

        ob = ob or {}
        accessor = self._get_accessor(sheet_url)
        extractor = Extractor(introspector)
        for section in introspector.section_names:
            rows = extractor.extract_rows_with_config_data(ob, section)
            accessor.store_rows(rows, section)

    @reify
    def client(self) -> Client:
        from gspread.auth import (
            InstalledAppFlow,
            load_credentials,
            store_credentials,
            Client,
        )

        authorized_user_path = pathlib.Path(self.authorized_user_filename).expanduser()
        credential_path = pathlib.Path(self.credential_filename).expanduser()
        if not authorized_user_path.parent.exists():
            authorized_user_path.parent.mkdir(parents=True)
        if not credential_path.parent.exists():
            credential_path.parent.mkdir(parents=True)

        creds = load_credentials(filename=str(authorized_user_path))

        if not creds:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(credential_path), self.scopes
                )
            except FileNotFoundError as e:
                raise exceptions.CredentialsFileIsNotFound(e.filename)

            creds = flow.run_local_server(port=self.port)
            store_credentials(creds, filename=str(authorized_user_path))

        client = Client(auth=creds)
        return client
