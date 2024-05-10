# Claudio Perez
__version__ = "0.1.18"

from pathlib import Path
from functools import reduce
import importlib

from . import csmip, nga, eqsig, basic_formats, opensees

FILE_TYPES = {}

# Avoid repeated dot lookup
_register_file_type = FILE_TYPES.update
_register_file_type(nga.FILE_TYPES)
_register_file_type(csmip.FILE_TYPES)
_register_file_type(eqsig.FILE_TYPES)
_register_file_type(basic_formats.FILE_TYPES)
_register_file_type(opensees.FILE_TYPES)

# Map different file extensions to the name
# of the parser that should be used by default
# (when format argument is not explicitly passed).
DEFAULT_TYPES = {
    ".at2":  "nga.at2",
    ".AT2":  "nga.at2",
    ".zip":  "csmip.zip",
    ".v2":   "csmip.v2",
    ".V2":   "csmip.v2",
    ".json": "json",
}


def _find_function(module, name):
    try:
        func = reduce(getattr, name.split(".")[1:], module)
    except AttributeError:
        # only import if required
        importlib.import_module(module.__name__ + "." + name.rsplit(".",1)[0])
        func = reduce(getattr, name.split("."), module)
    # except Exception as e:
    #     print(e)
    return func

def aread(archive, sequence=("event","")):
    pass

def read(read_file, input_format=None, **kwds):
    """
    Generic ground motion reader
    """
    if "parser" in kwds and kwds["parser"] is not None:
        import quakeio
        return _find_function(quakeio, kwds["parser"])(read_file, **kwds)

    input_format = input_format or kwds.pop("format",None)
    if input_format is not None:
        typ = input_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(read_file).suffix.lower()]
        except KeyError:
            raise ValueError("Unable to deduce input format.\n")

    if typ in FILE_TYPES:
        return FILE_TYPES[typ]["read"](read_file, **kwds)

    raise Exception()



def write(write_file, ground_motion, write_format: str = None, *args, **kwds):
    """
    Generic ground motion writer
    """
    if write_format:
        typ = write_format
    else:
        try:
            typ = DEFAULT_TYPES[Path(write_file).suffix.lower()]
        except KeyError:
            raise ValueError("Unable to deduce output format")
    FILE_TYPES[typ]["write"](write_file, ground_motion, *args, **kwds)

def dumps(ground_motion, **kwds):
    return basic_formats.dumps_json(ground_motion, **kwds)

