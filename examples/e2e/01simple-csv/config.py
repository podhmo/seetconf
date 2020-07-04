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
