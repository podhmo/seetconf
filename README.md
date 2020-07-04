# sheetconf

:construction: this project is under construction :construction:

## how to use it

- [./examples/e2e](./examples/e2e)

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
loader = sheetconf.get_loader(format="spreadsheet")
config = sheetconf.loadfile(url, parser=Parser(Config, loader=loader), adjust=True)

print(config)
# Config(logger=LoggerConfig(level='INFO'), xxx=XXXConfig(name='xxx', token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'), yyy=YYYConfig(name='yyy', token='yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'))
```
