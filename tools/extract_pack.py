"""A tool to extract sub-files from a PMD2 pack file."""

from collections import deque
from pathlib import Path

import click
from kaitaistruct import KaitaiStructError
from pkdpx import Pkdpx
from pmd2pack import Pmd2pack


def decompress(data: bytes, control_flags: bytes) -> bytes:
    """Decompress PKDPX files which use PMD2 PX compression."""

    in_queue = deque(data)
    out = []

    while in_queue:
        command_byte = in_queue.popleft()
        mask = 0x80

        while mask > 0:
            if not in_queue:
                break

            bitval = command_byte & mask
            mask >>= 1

            if bitval:
                # Copy next byte.
                out.append(in_queue.popleft())

            else:
                # Process next byte.
                byte = in_queue.popleft()
                nbhigh = (byte >> 4) & 0xF
                nblow = byte & 0xF

                if nbhigh in control_flags:
                    ctrlflagindex = control_flags.index(nbhigh)

                    if ctrlflagindex == 0:
                        # Insert byte pattern.
                        byte1 = (nblow << 4) | nblow
                        byte2 = byte1
                        out.extend([byte1, byte2])
                    else:
                        # Insert special byte pattern.
                        basenybbleval = nblow
                        if ctrlflagindex == 1:
                            basenybbleval += 1
                        elif ctrlflagindex == 5:
                            basenybbleval -= 1

                        nybbles = [basenybbleval] * 4

                        if 1 <= ctrlflagindex <= 4:
                            nybbles[ctrlflagindex - 1] -= 1
                        else:
                            nybbles[ctrlflagindex - 5] += 1

                        byte1 = (nybbles[0] << 4) | nybbles[1]
                        byte2 = (nybbles[2] << 4) | nybbles[3]
                        out.extend([byte1, byte2])

                else:
                    # Copy sequence.
                    if not in_queue:
                        break
                    offset_byte = in_queue.popleft()
                    offset = ((nblow << 8) | offset_byte) - 0x1000
                    seqbeg = len(out) + offset

                    length = nbhigh + 3

                    for i in range(length):
                        src_index = seqbeg + i
                        out.append(out[src_index])

    return bytes(out)


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
        try:
            pkdpx = Pkdpx.from_bytes(file.data)
            output_data = decompress(pkdpx.data, pkdpx.controls_flags)
        except KaitaiStructError:
            output_data = file.data

        open(extract_path / str(i), "wb").write(output_data)


if __name__ == "__main__":
    main()
