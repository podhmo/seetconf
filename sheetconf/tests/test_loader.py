# type: ignore
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


def test_csv_loader():
    from sheetconf import CSVLoader

    basedir = str(get_testdata_path("./testdata/csv-config"))
    dummy_section_names = ["slack-xxx-bot"]

    class DummyIntrospector:
        section_names = dummy_section_names

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
