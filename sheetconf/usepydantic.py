import typing as t
import pydantic
from .types import Loader, RowDict
from .langhelpers import zero_value

ConfigT = t.TypeVar("ConfigT", bound=pydantic.BaseModel)


class Introspector:
    def __init__(self, schema_class: t.Type[ConfigT]) -> None:
        self.schema_class = schema_class

    @property
    def section_names(self) -> t.List[str]:
        return [name for name, field in self.schema_class.__fields__.items()]

    def get_fields(self, section_name: str) -> t.Iterator[RowDict]:
        sub_schema: t.Type[ConfigT] = self.schema_class.__fields__[section_name].type_
        for name, field in sub_schema.__fields__.items():
            description = field.field_info.description
            value = None
            if (
                not field.required
                and not field.field_info.const
                and field.default is not None
            ):
                value = field.default
            if value is None and field.required:
                value = zero_value(field.type_)

            typ = field.type_
            if hasattr(typ, "__origin__"):  # for Literal
                if value is None:
                    value = typ.__args__[0]
                typ = type(typ.__args__[0])

            row: RowDict = {
                "name": name,
                "value": value,
                "value_type": typ.__name__,  # xxx
                "description": description,
            }
            yield row


class Parser(t.Generic[ConfigT]):
    def __init__(self, schema_class: t.Type[ConfigT], *, loader: Loader) -> None:
        self.introspector = Introspector(schema_class)
        self.schema_class = schema_class
        self.loader = loader

    @property
    def section_names(self) -> t.List[str]:
        return self.introspector.section_names

    def get_fields(self, section_name: str) -> t.Iterator[RowDict]:
        return self.introspector.get_fields(section_name)

    def parse(self, filename: str) -> ConfigT:
        data = self.loader.load(filename, parser=self)
        return self.schema_class.parse_obj(data)

    def unparse(
        self, ob: t.Union[ConfigT, t.Type[ConfigT]], filename: t.Optional[str] = None
    ) -> ConfigT:
        data = None
        if not isinstance(ob, type):
            data = ob.dict()
        self.loader.dump(data, filename, parser=self)
