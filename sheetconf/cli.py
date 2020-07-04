import typing as t
from handofcats import as_subcommand


def _get_printter(module_path: str) -> t.Callable[..., t.Any]:
    from importlib import import_module

    mod, sym = module_path.rsplit(":", 1)
    printer = getattr(import_module(mod), sym)
    return printer  # type: ignore


@as_subcommand  # type: ignore
def load(
    filename: str, *, format: str = "json", printer: str = "pprint:pprint"
) -> None:
    from sheetconf import JSONLoader, RawParser, load

    print_function = _get_printter(printer)

    data = load(filename, parser=RawParser(JSONLoader()))

    print_function(data)


as_subcommand.run()
