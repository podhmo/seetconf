# type: ignore
import typing as t
from sheetconf.tests.testutils import get_testdata_path


def test_json_loader():
    from sheetconf import JSONLoader

    filename = str(get_testdata_path("./testdata/config.json"))
    dummy_introspector = None

    loader = JSONLoader()
    got = loader.load(filename, introspector=dummy_introspector, adjust=False)

    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "version": 11,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    assert got == want


def test_rows_loader():
    from sheetconf import RowsLoader
    from sheetconf.types import RowDict

    dummy_filename = "*filename*"
    dummy_section_names = ["slack-xxx-bot"]

    rows_dict: t.Dict[str, t.Iterator[RowDict]] = {
        "slack-xxx-bot": [
            {
                "name": "name",
                "value": "someone",
                "value_type": "str",
                "description": None,
            },
            {
                "name": "version",
                "value": "11",
                "value_type": "int",
                "description": None,
            },
            {
                "name": "token",
                "value": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "value_type": "str",
                "description": None,
            },
        ]
    }

    class DummyIntrospector:
        section_names = dummy_section_names

    def get_rows(filename: str, section: str) -> t.Iterator[RowDict]:
        assert filename == dummy_filename
        return rows_dict[section]

    loader = RowsLoader(get_rows)
    got = loader.load(dummy_filename, introspector=DummyIntrospector(), adjust=False)
    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "version": 11,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    print(got)
    assert got == want
