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
    def load(self, source: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        ...

    def dump(
        self,
        ob: t.Optional[t.Dict[str, t.Any]],
        filename: t.Optional[str] = None,
        *,
        parser: Parser[t.Any],
    ) -> None:
        ...


class Fetcher(tx.Protocol):
    def fetch(self, section_name: str) -> t.Iterator[RowDict]:
        ...


class Parser(tx.Protocol[ConfigT]):
    @property
    def section_names(self) -> t.List[str]:
        ...

    def get_fields(self, section_name: str) -> t.Iterator[RowDict]:
        ...

    def parse(self, filename: str) -> ConfigT:
        ...

    def unparse(self, ob: t.Any, filename: t.Optional[str] = None) -> None:
        ...
