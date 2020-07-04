import sys
import sheetconf
from sheetconf.usepydantic import Parser
from pydantic import BaseModel


class XXXConfig(BaseModel):
    name: str
    token: str


class YYYConfig(BaseModel):
    name: str
    token: str


class Config(BaseModel):
    xxx: XXXConfig
    yyy: YYYConfig


filename = sys.argv[1]
config = sheetconf.load(filename, parser=Parser(Config, loader=sheetconf.JSONLoader()))
print(config)
