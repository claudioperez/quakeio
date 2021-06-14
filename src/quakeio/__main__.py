import argparse
import quakeio


def build_parser():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="quakeio", description="Ground motion processing utilities."
    )
    parser.add_argument("read_file", nargs="?", default="-")
    parser.add_argument("-o", "--write_file", default="-")
    parser.add_argument("-c", "--command", action="append")
    parser.add_argument("-S", "--summarize", action="store_true")
    parser.add_argument(
        "-f",
        dest="input_format",
        help="Specity input file format",
        choices=list(quakeio.FILE_TYPES.keys()),
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="write_format",
        help="Specity output file format",
        default="json.record",
    )
    parser.add_argument("-s", "--scale", help="Scale ground motions by factor FACTOR")

    parser.add_argument(
        "--version", help="Print version and exit.", action="store_true"
    )
    # fmt: on
    return parser


def cli(*args, **kwds):
    if kwds["version"]:
        print(quakeio.__version__)
        return
    if "command" in kwds:
        cmds = kwds.pop("command")

    write_file = kwds["write_file"]
    del kwds["write_file"]
    motion = quakeio.read(**kwds)
    quakeio.write(write_file, motion, **kwds)
    print("\n")


def main():
    args = build_parser().parse_args()
    cli(**vars(args))


if __name__ == "__main__":
    main()
