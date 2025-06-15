"""A tool to extract strings from a `.str` file."""

import click
from str_format import StrFormat


def parse_string(string_pointer: StrFormat.StringPointer) -> str:
    try:
        return string_pointer.string
    except UnicodeDecodeError:
        return "\t[STRING CAN'T BE DECODED]"


@click.group()
def cli() -> None:
    """Extract strings from a `.str` file."""


@cli.command(help="Lists all strings in the file.")
@click.argument("str_file", type=str)
def all(str_file: str) -> None:
    extract_string_file = StrFormat.from_file(str_file)

    for i, string_pointer in enumerate(extract_string_file.strings):
        string = parse_string(string_pointer)
        print(f"{i}\t{string}")


@cli.command(help="Get the string at the given index.")
@click.argument("str_file", type=str)
@click.argument("index", type=int)
def at_index(str_file: str, index: int) -> None:
    extract_string_file = StrFormat.from_file(str_file)

    string = parse_string(extract_string_file.strings[index])

    print(string)


if __name__ == "__main__":
    cli()
