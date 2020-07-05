import typing_extensions as tx
from pydantic import BaseModel, Field


class LoggerConfig(BaseModel):
    level: tx.Literal["DEBUG", "INFO", "WARNING", "ERROR"]


class XXXConfig(BaseModel):
    name: str
    token: str


class YYYConfig(BaseModel):
    name: str = Field(default="yyy")
    token: str = Field(
        default="yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
        description="access token of yyy",
    )


class Config(BaseModel):
    logger: LoggerConfig
    xxx: XXXConfig
    yyy: YYYConfig
