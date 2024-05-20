# Claudio Perez
# Command line interface for QuakeIO tool
import argparse
import sys
import quakeio


def build_parser():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="quakeio",
        description="""Parsers and utilities for processing and converting accelerograms.

        """,
        usage="quakeio [MODE] [OPTIONS] FILE"
    )
    modes = parser.add_argument_group("Modes")
    modes.add_argument("-A", "--all", dest="mode_process", action="store_true",
        help="Process all input data [default]"
    )
    modes.add_argument("-S", "--summarize", action="store_true",
        help="Omit time series data and superfluous fields from output"
    )
    modes.add_argument("-v", "--verbose", dest="verbosity", action="count", default=0,
        help="Increase output verbosity"
    )

    parser.add_argument("read_file", metavar="FILE", nargs="?", default="-")
    #parser.add_argument("-c", dest="command", action="append")
    #parser.add_argument("validate", action="store_true", default=False
    #)
    parser.add_argument(
        "-f",
        dest="input_format",
        metavar="FORMAT",
        help="Specify input file format",
        choices=list(quakeio.FILE_TYPES.keys()),
    )
    parser.add_argument(
        "-t", "--to",
        dest="write_format",
        metavar="FORMAT",
        help="Specify output file format",
        default="json",
    )
    parser.add_argument(
            "--human",
            default=False,
            action="store_true",
            help="Use human friendly field names."
    )
    parser.add_argument(
        "-x",
        "--exclude",
        dest="exclusions",
        metavar="KEY",
        help="Specify keys to exclude by parser",
        action="append",
        default=[]
    )
    parser.add_argument(
            "-m",
            dest="match_patterns",
            action="append",
            default=[]
    )
    parser.add_argument(
            "-o",
            dest="write_file",
            default="-",
            help="Specify an output file."
    )
    parser.add_argument(
            "-p",
            "--parser",
            dest="parser",
            default=None,
            help="Specify a parser."
    )
    parser.add_argument(
        "-r",
        "--rotate",
        dest="angle",
        metavar="ANGLE",
        help="Rotate grouped records by ANGLE"
    )
    # parser.add_argument("-s", "--scale", help="Scale ground motions by factor FACTOR")

    parser.add_argument(
        "--version", help="Print version and exit.", action="version", version=quakeio.__version__
    )
    formats = parser.add_argument_group("Formats",
        description=f"""
        yaml, json, csmip, opensees
        """
        # {', '.join(quakeio.FILE_TYPES.keys())}
    )
    # fmt: on
    return parser


def cli(*args, write_file="-", human=False, validate=False, version=False, command=None, **kwds):
    read_file = kwds.pop("read_file")
    if "?" in read_file:
        from urllib.parse import urlparse
        url = urlparse(read_file)
        read_file = url.path
        query = url.query
    else:
        query = None

    motion = quakeio.read(read_file, **kwds)

    if kwds["match_patterns"]:
        kvs = {}
        for pat in kwds["match_patterns"]:
            key, val = pat.split("=")
            try:
                key, typ = key.split(":")
            except:
                typ = "l"
            kvs.update({key: val})
            motion = motion.match(typ, **kvs)
            if motion is not None:
                break
        else:
            print(f"No match for pattern {kwds['match_patterns']}", file=sys.stderr)
            sys.exit(-1)

    if validate:
        run_validation(motion)

    if human:
        motion = quakeio.core.write_pretty(motion)

    if "angle" in kwds and kwds["angle"]:
        quakeio.core.rotate(motion, float(kwds["angle"]))


    quakeio.write(write_file, motion, **kwds)
    print("\n")

def run_validation(collection):
    for motion in collection.motions:
        for component in motion.components:
            for series in component.series:
                pass
    pass

def list_args(*args):
    args = build_parser().parse_args()
    return cli(**vars(args))

def main(args=None):
    args = build_parser().parse_args(args)
    try:
        cli(**vars(args))
    except Exception as e:
        print(args)
        raise e


if __name__ == "__main__":
    main()
