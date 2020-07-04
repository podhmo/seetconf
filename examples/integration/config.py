import typing_extensions as tx
from pydantic import BaseModel, Field


class XXXConfig(BaseModel):
    name: str
    token: str = Field(description="token of xxx api")


class YYYConfig(BaseModel):
    name: str
    token: str = Field(description="token of xxx api")


class LoggerConfig(BaseModel):
    level: tx.Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class Config(BaseModel):
    logger: LoggerConfig
    xxx: XXXConfig
    yyy: YYYConfig
