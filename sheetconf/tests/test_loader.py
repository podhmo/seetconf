# type: ignore
from sheetconf.tests.testutils import get_testdata_path


def test_json_loader():
    from sheetconf import JSONLoader

    filename = str(get_testdata_path("./testdata/config.json"))
    dummy_parser = None

    loader = JSONLoader()
    got = loader.load(filename, parser=dummy_parser)

    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    assert got == want
