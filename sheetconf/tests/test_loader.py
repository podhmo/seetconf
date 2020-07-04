# type: ignore
from sheetconf.tests.testutils import get_testdata_path


def test_json_loader():
    from sheetconf import JSONLoader

    filename = str(get_testdata_path("./testdata/config.json"))
    loader = JSONLoader()

    got = loader.load(filename)
    want = {
        "slack-xxx-bot": {
            "name": "someone",
            "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    }
    assert got == want
