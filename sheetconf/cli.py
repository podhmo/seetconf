import typing as t
import typing_extensions as tx
import sys
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
def schema(*, config: str) -> None:
    import json
    from pydantic.schema import schema

    config_class = t.cast(t.Type[t.Any], _import_symbol(config))
    schema_dict = schema([config_class])
    schema_dict["$ref"] = f"#/definitions/{config_class.__name__}"

    print(json.dumps(schema_dict, indent=2, ensure_ascii=False))
    print()


@as_subcommand  # type: ignore
def init(
    filename: str, *, config: str, format: tx.Literal["json", "csv", "spreadsheet"]
) -> None:
    from sheetconf import savefile, get_loader
    from sheetconf.usepydantic import Parser

    config_class = t.cast(t.Type[t.Any], _import_symbol(config))

    loader = get_loader(format=format)
    parser = Parser(config_class, loader=loader)

    savefile(config_class, filename, parser=parser)


@as_subcommand  # type: ignore
def load(
    filename: str,
    *,
    config: str,
    format: tx.Literal["json", "csv", "spreadsheet"],
    adjust: bool = False,
    printer: str = "pprint:pprint",
) -> None:
    import pydantic
    from sheetconf import loadfile, get_loader
    from sheetconf.usepydantic import Parser

    print_function = t.cast(t.Callable[..., None], _import_symbol(printer))
    config_class = t.cast(t.Type[t.Any], _import_symbol(config))

    loader = get_loader(format=format)
    parser = Parser(config_class, loader=loader)

    try:
        data = loadfile(filename, parser=parser, adjust=adjust)
    except pydantic.ValidationError as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    print_function(data)


as_subcommand.run()
