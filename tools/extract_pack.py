"""A tool to extract sub-files from a PMD2 pack file."""

from pathlib import Path

import click
from pmd2pack import Pmd2pack


@click.command()
@click.argument("pack_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("output_dir", type=click.Path(file_okay=False))
def main(pack_file: str, output_dir: str) -> None:
    pack = Pmd2pack.from_file(pack_file)

    extract_folder = Path(pack_file).name + "_extract"
    extract_path = Path(output_dir) / extract_folder
    extract_path.mkdir(parents=True, exist_ok=True)

    file: Pmd2pack.File
    for i, file in enumerate(pack.files):
        open(extract_path / str(i), "wb").write(file.data)


if __name__ == "__main__":
    main()
