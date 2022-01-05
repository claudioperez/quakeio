import re
import io
from os import PathLike
from pathlib import Path
from typing import Union, IO, Callable
import contextlib

# Regular expression for extracting decimal number
RE_DECIMAL = "[-]?[0-9]*[.]?[0-9]*"
# Regular expression for extracting units
RE_UNITS = "[A-z,/,0-9]*"

CRE_WHITE = re.compile("\\W+")


def maybe_t(pattern: str, typ: Callable, strict: bool = True):
    cpattern = re.compile(pattern, re.IGNORECASE)
    def proc(match):
        if match:
            return typ(re.search(cpattern, match).group(1))
        else:
            return None

    return proc


@contextlib.contextmanager
def open_quake(file, mode=None, archive=None):
    import sys

    if file == "-":
        if mode is None or mode == "" or "r" in mode:
            fh = sys.stdin
        else:
            fh = sys.stdout
    elif not archive and isinstance(file, (PathLike, str)):
        fh = open(file, mode)
    elif archive:
        fh = archive.open(file, mode)
    else:
        fh = file
    # if file != "-":
    #     yield fh
    #     fh.close()
    try:
        yield fh

    finally:
        if isinstance(file, str) and file != "-":
            fh.close()


def parse_sequential_fields(data, field_spec: dict, parsed_fields={}) -> dict:
    """ """
    field_iterator = iter(field_spec.items())
    fields, (typs, regex) = next(field_iterator)
    for line in data:
        match = regex.findall(str(line))
        if match:
            prefix = ""
            assert len(fields) == len(typs) == len(match[0]), (regex, match[0])
            for field, typ, val in zip(fields, typs, match[0]):
                if field[0] == ".":
                    key = prefix + field
                else:
                    prefix = field
                    key = field

                parsed_fields[key] = typ(val)
            try:
                fields, (typs, regex) = next(field_iterator)
            except StopIteration:
                # All fields have been parsed out
                break
        else:
            pass
    return parsed_fields


def parse_sequential_fields_v0(data, fields, parsed_fields={}):
    """ """
    field_iterator = iter(fields.items())
    field, (keys, typs, regex) = next(field_iterator)

    for line in data:
        match = regex.findall(str(line))
        if match:
            parsed_fields[field] = {
                key: typ(val) for key, typ, val in zip(keys, typs, match[0])
            }
            try:
                field, (keys, typs, regex) = next(field_iterator)
            except StopIteration:
                # All fields have been parsed out
                break
    return parsed_fields


def get_file_type(
    file: Union[str, Path, IO], file_type: str, module: str = None
) -> str:
    if isinstance(file, io.IOBase):
        return file_type
