from pydantic import BaseModel, Field


class XXXConfig(BaseModel):
    name: str
    token: str = Field(description="token of xxx api")


class Config(BaseModel):
    xxx: XXXConfig
