from __future__ import annotations
import typing as t
import typing_extensions as tx


ConfigT = t.TypeVar("ConfigT", covariant=True)


class RowDict(tx.TypedDict, total=True):
    name: str
    value: t.Optional[str]
    value_type: tx.Literal["int", "str", "float"]
    description: t.Optional[str]


class Loader(tx.Protocol):
    def load(
        self, source: str, *, introspector: Introspector, adjust: bool
    ) -> t.Dict[str, t.Any]:
        ...

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        filename: t.Optional[str] = None,
        *,
        introspector: Introspector,
    ) -> None:
        ...


class Introspector(tx.Protocol):
    @property
    def section_names(self) -> t.List[str]:
        ...

    def get_fields(self, section_name: str) -> t.Iterator[RowDict]:
        ...


class Parser(tx.Protocol[ConfigT]):
    def parse(self, filename: str, *, adjust: bool = False) -> ConfigT:
        ...

    def unparse(self, ob: t.Any, filename: t.Optional[str] = None) -> None:
        ...
