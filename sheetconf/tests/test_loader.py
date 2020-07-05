# type: ignore
from sheetconf.tests.testutils import get_testdata_path


def test_json_loader():
    from sheetconf import JSONLoader

    filename = str(get_testdata_path("./testdata/config.json"))

    class DummyIntrospector:
        section_names = ["slack-xxx-bot"]

        def get_fields(self, section: str):
            return []

    loader = JSONLoader()
    got = loader.load(filename, introspector=DummyIntrospector(), adjust=False)

    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "version": 11,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    assert got == want


def test_csv_loader():
    from sheetconf import CSVLoader

    basedir = str(get_testdata_path("./testdata/csv-config"))

    class DummyIntrospector:
        section_names = ["slack-xxx-bot"]

    loader = CSVLoader()
    got = loader.load(basedir, introspector=DummyIntrospector(), adjust=False)
    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "version": 11,
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    assert got == want
