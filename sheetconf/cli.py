import typing as t
from handofcats import as_subcommand


def _get_printter(module_path: str) -> t.Callable[..., t.Any]:
    from importlib import import_module

    mod, sym = module_path.rsplit(":", 1)
    return getattr(import_module(mod), sym)


@as_subcommand
def load(
    filename: str, *, format: str = "json", printer: str = "pprint:pprint"
) -> None:
    from sheetconf import JSONLoader

    print_function = _get_printter(printer)

    loader = JSONLoader()
    data = loader.load(filename)

    print_function(data)


as_subcommand.run()
