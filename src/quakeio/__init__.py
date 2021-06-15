# Claudio Perez
__version__ = "0.0.2"

from pathlib import Path

from . import (
    csmip,
    # nga,
    eqsig,
    basic_formats,
)


FILE_TYPES = {}
FILE_TYPES.update(csmip.FILE_TYPES)
FILE_TYPES.update(eqsig.FILE_TYPES)
FILE_TYPES.update(basic_formats.FILE_TYPES)

DEFAULT_TYPES = {
    ".zip":  "csmip.zip",
    ".v2":   "csmip.v2",
    ".json": "json",
}


def read(read_file, input_format=None, **kwds):
    """
    Generic ground motion reader
    """
    if input_format:
        typ = input_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(read_file).suffix]
        except KeyError:
            raise ValueError("Unable to deduce input format")
    return FILE_TYPES[typ]["read"](read_file, **kwds)


def write(write_file, ground_motion, write_format=None, *args, **kwds):
    if write_format:
        typ = write_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(write_file).suffix]
        except KeyError:
            raise ValueError("Unable to deduce output format")
    FILE_TYPES[typ]["write"](write_file, ground_motion, *args, **kwds)
