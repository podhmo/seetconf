import typing as t
from functools import update_wrapper

T = t.TypeVar("T")


# stolen from pyramid
class reify(t.Generic[T]):
    """cached property"""

    def __init__(self, wrapped: t.Callable[[t.Any], T]):
        self.wrapped = wrapped
        update_wrapper(self, wrapped)  # type: ignore

    def __get__(
        self, inst: t.Optional[object], objtype: t.Optional[t.Type[t.Any]] = None
    ) -> T:
        if inst is None:
            return self  # type: ignore
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


ZERO_MAPPING = {
    int: 0,
    float: 0.0,
    str: "",
}


def zero_value(
    typ: t.Type[t.Any], *, mapping: t.Optional[t.Dict[t.Type[t.Any], t.Any]] = None
) -> t.Any:
    mapping = mapping or ZERO_MAPPING
    return mapping.get(typ)


TRANSLATE_MAPPING: t.Dict[str, t.Callable[[t.Any], t.Any]] = {
    "float": float,
    "int": int,
    "str": str,
}  # todo: refinement


def get_translate_function(
    s: str, *, mapping: t.Optional[t.Dict[str, t.Callable[[t.Any], t.Any]]] = None
) -> t.Callable[[t.Any], t.Any]:
    mapping = mapping or TRANSLATE_MAPPING
    return mapping.get(s) or str
