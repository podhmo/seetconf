import typing_extensions as tx
from pydantic import BaseModel, Field
import sheetconf
from sheetconf.usepydantic import Introspector, Parser


class LoggerConfig(BaseModel):
    level: tx.Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class XXXConfig(BaseModel):
    name: str
    token: str


class YYYConfig(BaseModel):
    name: str = Field(description="name of yyy")
    token: str = Field(
        description="token of yyy", default="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
    )


class Config(BaseModel):
    logger: LoggerConfig
    xxx: XXXConfig
    yyy: YYYConfig


ob = Config.parse_obj(
    {
        "logger": {"level": "DEBUG"},
        "xxx": {"name": "xxx", "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"},
        "yyy": {"name": "yyy", "token": "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"},
    }
)

p = Parser(Config, loader=sheetconf.JSONLoader())
p.unparse(ob)

print("----------------------------------------")

p = Parser(Config, loader=sheetconf.CSVLoader())
p.unparse(ob)
