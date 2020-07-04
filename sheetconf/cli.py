import typing as t
import typing_extensions as tx
from handofcats import as_subcommand


def _get_printter(module_path: str) -> t.Callable[..., t.Any]:
    from importlib import import_module

    mod, sym = module_path.rsplit(":", 1)
    printer = getattr(import_module(mod), sym)
    return printer  # type: ignore


@as_subcommand  # type: ignore
def load(
    filename: str, *, format: tx.Literal["json", "csv"], printer: str = "pprint:pprint"
) -> None:
    from sheetconf import RawParser, loadfile

    print_function = _get_printter(printer)

    if format == "json":
        from sheetconf import JSONLoader

        data = loadfile(filename, parser=RawParser(JSONLoader()))
    elif format == "csv":
        import pathlib
        from sheetconf import CSVLoader

        section_names = [p.stem for p in pathlib.Path(filename).glob("*.csv")]
        data = loadfile(
            filename,
            parser=RawParser(CSVLoader(ext=".csv"), section_names=section_names),
        )

    print_function(data)


as_subcommand.run()
