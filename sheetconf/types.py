from __future__ import annotations
import typing as t
import typing_extensions as tx


ConfigT = t.TypeVar("ConfigT")


class Loader(tx.Protocol):
    def load(self, source: str) -> t.Dict[str, t.Any]:
        ...


class Fetcher(tx.Protocol):
    def fetch(self, url: str) -> t.Dict[str, t.Any]:
        ...


class Parser(tx.Protocol[ConfigT]):
    def parse(self, data: t.Dict[str, t.Any]) -> ConfigT:
        ...
