import pathlib


def get_testdata_path(filename: str) -> pathlib.Path:
    return pathlib.Path(__file__).parent.absolute() / (filename)
