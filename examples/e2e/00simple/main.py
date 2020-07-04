import sys
from sheetconf import JSONLoader
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
data = JSONLoader().load(filename)
config = Config.parse_obj(data)
print(config)
