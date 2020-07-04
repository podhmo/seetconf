import typing as t
import typing_extensions as tx
from handofcats import as_subcommand


def _import_symbol(module_path: str) -> object:
    path, sym = module_path.rsplit(":", 1)

    if ".py:" in module_path:
        import runpy

        ob = runpy.run_path(path)[sym]
    else:
        from importlib import import_module

        ob = getattr(import_module(path), sym)
    return ob


@as_subcommand  # type: ignore
def load(
    filename: str,
    *,
    config: str,
    format: tx.Literal["json", "csv"],
    printer: str = "pprint:pprint"
) -> None:
    from sheetconf import loadfile
    from sheetconf.usepydantic import Parser

    print_function = _import_symbol(printer)  # type: t.Callable[..., None]
    config_class = _import_symbol(config)  # type: t.Type[t.Any]

    if format == "json":
        from sheetconf import JSONLoader

        data = loadfile(filename, parser=Parser(config_class, loader=JSONLoader()))
    elif format == "csv":
        from sheetconf import CSVLoader

        data = loadfile(
            filename, parser=Parser(config_class, loader=CSVLoader(ext=".csv")),
        )

    print_function(data)


as_subcommand.run()
