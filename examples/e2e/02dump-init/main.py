import typing_extensions as tx
import os
from pydantic import BaseModel, Field
import sheetconf
from sheetconf.usepydantic import Parser


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


p = Parser(Config, loader=sheetconf.JSONLoader())
p.unparse(Config)

print("----------------------------------------")

p = Parser(Config, loader=sheetconf.CSVLoader())
p.unparse(Config)

if bool(os.getenv("USESHEET")):
    from sheetconf.usegspread import Loader

    p = Parser(Config, loader=Loader())
    p.unparse(
        Config,
        "https://docs.google.com/spreadsheets/d/1xLb9Sa_3PKgq_FzXatE4_UFC1hSLjcwdG1Lp4P7Ttpw/edit#gid=0",
    )
