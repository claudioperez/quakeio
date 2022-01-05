# Claudio Perez
__version__ = "0.1.3"

from pathlib import Path

from . import csmip, nga, eqsig, basic_formats, opensees


FILE_TYPES = {}
# Avoid repeated dot lookup
_register_file_type = FILE_TYPES.update
_register_file_type(nga.FILE_TYPES)
_register_file_type(csmip.FILE_TYPES)
_register_file_type(eqsig.FILE_TYPES)
_register_file_type(basic_formats.FILE_TYPES)
_register_file_type(opensees.FILE_TYPES)

DEFAULT_TYPES = {
    ".at2": "nga.at2",
    ".AT2": "nga.at2",
    ".zip": "csmip.zip",
    ".v2": "csmip.v2",
    ".V2": "csmip.v2",
    ".json": "json",
}


def read(read_file, input_format=None, **kwds):
    """
    Generic ground motion reader
    """
    if input_format is not None:
        typ = input_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(read_file).suffix]
        except KeyError:
            raise ValueError("Unable to deduce input format")
    return FILE_TYPES[typ]["read"](read_file, **kwds)


def write(write_file, ground_motion, write_format: str = None, *args, **kwds):
    """
    Generic ground motion writer
    """
    if write_format:
        typ = write_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(write_file).suffix]
        except KeyError:
            raise ValueError("Unable to deduce output format")
    FILE_TYPES[typ]["write"](write_file, ground_motion, *args, **kwds)

def dumps(ground_motion, **kwds):
    return basic_formats.dumps_json(ground_motion, **kwds)


