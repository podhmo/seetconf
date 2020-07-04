import typing as t
import pydantic
from .types import Loader

ConfigT = t.TypeVar("ConfigT", bound=pydantic.BaseModel)


class Parser(t.Generic[ConfigT]):
    def __init__(self, schema_class: t.Type[ConfigT], *, loader: Loader) -> None:
        self.schema_class = schema_class
        self.loader = loader

    def parse(self, filename: str) -> ConfigT:
        data = self.loader.load(filename)
        return self.schema_class.parse_obj(data)
