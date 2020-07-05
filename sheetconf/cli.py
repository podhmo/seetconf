import typing as t

import typing_extensions as tx
import sys



def _import_symbol(module_path: str) -> object:
    path, sym = module_path.rsplit(":", 1)

    if ".py:" in module_path:
        import runpy

        ob = runpy.run_path(path)[sym]
    else:
        from importlib import import_module

        ob = getattr(import_module(path), sym)
    return ob


def schema(*, config: str) -> None:
    import json
    from pydantic.schema import schema

    config_class = t.cast(t.Type[t.Any], _import_symbol(config))
    schema_dict = schema([config_class])
    schema_dict["$ref"] = f"#/definitions/{config_class.__name__}"

    print(json.dumps(schema_dict, indent=2, ensure_ascii=False))
    print()


def init(
    filename: str, *, config: str, format: tx.Literal["json", "csv", "spreadsheet"]
) -> None:
    from sheetconf import savefile, get_loader
    from sheetconf.usepydantic import Parser

    config_class = t.cast(t.Type[t.Any], _import_symbol(config))

    loader = get_loader(format=format)
    parser = Parser(config_class, loader=loader)

    savefile(config_class, filename, parser=parser)


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


def main(argv: t.Optional[t.List[str]] = None) -> t.Any:
    import argparse

    parser = argparse.ArgumentParser(formatter_class=type('_HelpFormatter', (argparse.ArgumentDefaultsHelpFormatter, argparse.RawTextHelpFormatter), {}))
    parser.print_usage = parser.print_help  # type: ignore
    subparsers = parser.add_subparsers(title='subcommands', dest='subcommand')
    subparsers.required = True

    fn = schema
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__, formatter_class=parser.formatter_class)
    sub_parser.add_argument('--config', required=True, help='-')
    sub_parser.set_defaults(subcommand=fn)

    fn = init  # type: ignore
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__, formatter_class=parser.formatter_class)
    sub_parser.add_argument('filename', help='-')
    sub_parser.add_argument('--config', required=True, help='-')
    sub_parser.add_argument('--format', required=True, choices=["'json'", "'csv'", "'spreadsheet'"], help='-')
    sub_parser.set_defaults(subcommand=fn)

    fn = load  # type: ignore
    sub_parser = subparsers.add_parser(fn.__name__, help=fn.__doc__, formatter_class=parser.formatter_class)
    sub_parser.add_argument('filename', help='-')
    sub_parser.add_argument('--config', required=True, help='-')
    sub_parser.add_argument('--format', required=True, choices=["'json'", "'csv'", "'spreadsheet'"], help='-')
    sub_parser.add_argument('--adjust', action='store_true', help='-')
    sub_parser.add_argument('--printer', required=False, default='pprint:pprint', help='-')
    sub_parser.set_defaults(subcommand=fn)

    args = parser.parse_args(argv)
    params = vars(args).copy()
    subcommand = params.pop('subcommand')
    return subcommand(**params)


if __name__ == '__main__':
    main()
