![Python package](https://github.com/podhmo/sheetconf/workflows/Python%20package/badge.svg) [![PyPi version](https://img.shields.io/pypi/v/sheetconf.svg)](https://pypi.python.org/pypi/sheetconf) [![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/download/releases/3.7.0/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/en/stable/)


# sheetconf

spreadsheet as config

## how to use it

Get config object from spreadsheet something like below.
https://docs.google.com/spreadsheets/d/1PgLfX5POop6QjpgjDLE9wbSWWXJYcowxRBEpxmpG8og

```python
import sys
import typing_extensions as tx
import sheetconf
from sheetconf.usepydantic import Parser
from pydantic import BaseModel, Field


class XXXConfig(BaseModel):
    name: str
    token: str


class YYYConfig(BaseModel):
    name: str = Field(default="yyy", description="name of yyy")
    token: str = Field(description="token of yyy")


class LoggerConfig(BaseModel):
    level: tx.Literal["DEBUG","INFO", "WARNING", "ERROR"]


class Config(BaseModel):
    xxx: XXXConfig
    yyy: YYYConfig
    logger: LoggerConfig


url = "https://docs.google.com/spreadsheets/d/1PgLfX5POop6QjpgjDLE9wbSWWXJYcowxRBEpxmpG8og"
config = sheetconf.loadfile(url, config=Config, format="spreadsheet", adjust=True)

print(config)
# Config(logger=LoggerConfig(level='INFO'), xxx=XXXConfig(name='xxx', token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'), yyy=YYYConfig(name='yyy', token='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'))
```

## other

- [./examples/e2e](./examples/e2e)
