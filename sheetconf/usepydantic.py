import typing as t
import pydantic
from .types import Loader

ConfigT = t.TypeVar("ConfigT", bound=pydantic.BaseModel)


class Parser(t.Generic[ConfigT]):
    def __init__(self, schema_class: t.Type[ConfigT], *, loader: Loader) -> None:
        self.schema_class = schema_class
        self.loader = loader

    @property
    def section_names(self) -> t.List[str]:
        hints = t.get_type_hints(self.schema_class)
        return [name for name, typ in hints.items()]

    def parse(self, filename: str) -> ConfigT:
        data = self.loader.load(filename, parser=self)
        return self.schema_class.parse_obj(data)
