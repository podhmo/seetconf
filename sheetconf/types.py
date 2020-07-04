from __future__ import annotations
import typing as t
import typing_extensions as tx


ConfigT = t.TypeVar("ConfigT", covariant=True)


class Loader(tx.Protocol):
    def load(self, source: str, *, parser: Parser[t.Any]) -> t.Dict[str, t.Any]:
        ...


class Fetcher(tx.Protocol):
    def fetch(self, url: str) -> t.Dict[str, t.Any]:
        ...


class Parser(tx.Protocol[ConfigT]):
    @property
    def section_names(self) -> t.List[str]:
        ...

    def parse(self, filename: str) -> ConfigT:
        ...
