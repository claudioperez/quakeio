# Claudio Perez
# 2021
"""
Parse a CSMIP Volume 2 strong motion data file.
"""
import re
import sys
import fnmatch
import zipfile
from pathlib import Path
from collections import defaultdict

import numpy as np


from .core import (
    QuakeCollection,
    QuakeMotion,
    QuakeComponent,
    QuakeSeries,
    # RealNumber
)
from .utils.parseutils import (
    parse_sequential_fields,
    open_quake,
    RE_DECIMAL,  # Regular expression for extracting decimal values
    RE_UNITS,  # Regular expression for extracting units
    CRE_WHITE,
    maybe_t,
)

# Module constants
NUM_COLUMNS = 8
HEADER_END_LINE = 45

INTEGER_HEADER_START_LINE = 25
INTEGER_HEADER_END_LINE = 25+7
REAL_HEADER_END_LINE = 45

to_key = lambda strng: strng.strip().replace(" ", "_").lower()

words = lambda x: CRE_WHITE.sub(" ", str(x)).strip()
units = lambda x: str(x).strip().lower()

# fmt: off
# Dict[
#   Tuple[*[Key]],
#   Tuple[ Tuple[*[Type]], RegExp]
# ]
# leading key (ie key.split(".")[0]) determines whether
# field is part of record or accel/veloc/displ series.
HEADER_FIELDS = {
    # line 1
    ("_", "record.record_identifier"): ((str, str),
        re.compile(r"([A-z ]*) ([A-z0-9\-\.]*)", re.IGNORECASE)
    ),
    # line 6
    ("record.station.no", "record.station.coord"): ((str, str),
        re.compile(
            rf"Station No\. *([0-9]*) *({RE_DECIMAL}[NSEW]*, *{RE_DECIMAL}[NSEW]*)",
            re.IGNORECASE
        )
    ),
    # line 8
    ("record.channel", "record.component", "_", "record.station.channel", "record.location_name"): (
        (str, str, maybe_t("(Deg)",str), maybe_t("Sta Chn: ([0-9]*)", words), words),
        re.compile(
            rf"Chan *([0-9]*): *([A-z0-9]*) *(Deg)? *(.*) *Location: *([ -~]*)\s",
            re.IGNORECASE
        )
    ),
    # line 11
    ("record.instr_period", ".units"): ((float, units),
        re.compile(
            rf"Instr Period *= *({RE_DECIMAL}) *({RE_UNITS}),",
            re.IGNORECASE
        )
    ),
    # line 15
    (
        "filter.bandpass.point", 
        "filter.bandpass.point.units", 
        "filter.bandpass.limit_low",
        "filter.bandpass.limit_high",
        "filter.bandpass.limit.units"
    ) : (
        (float, units, float, float, units),
        re.compile(
            rf"Accelerogram bandpass filtered with *({RE_DECIMAL}) *({RE_UNITS}) pts at *({RE_DECIMAL}) and *({RE_DECIMAL}) *({RE_UNITS})\s",
            re.IGNORECASE
        )
    ),
    ("accel.peak_value", "accel.units", "accel.peak_time"): ((float, units, float),
        re.compile(
            rf"Peak *acceleration *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})",
            re.IGNORECASE
        )
    ),
    ("veloc.peak_value", "veloc.units", "veloc.peak_time"): ((float, units, float),
        re.compile(
            rf"Peak *velocity *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})",
            re.IGNORECASE
        )
    ),
    ("displ.peak_value", "displ.units", "displ.peak_time"): ((float, units, float),
        re.compile(
            rf"Peak *displacement *= *({RE_DECIMAL}) *({RE_UNITS}) *at *({RE_DECIMAL})",
            re.IGNORECASE
        )
    ),
    ("record.init_veloc", ".units", "record.init_displ", ".units"): ((float, units, float, units),
        re.compile(
            rf"Initial velocity *= *({RE_DECIMAL}) *({RE_UNITS}); *Initial displacement *= *({RE_DECIMAL}) *({RE_UNITS})\s",
            re.IGNORECASE
        )
    ),
    ("accel.shape", "accel.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of accel data equally spaced at *({RE_DECIMAL})", re.IGNORECASE)
    ),
    ("veloc.shape", "veloc.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of veloc data equally spaced at *({RE_DECIMAL})", re.IGNORECASE)
    ),
    ("displ.shape", "displ.time_step"): ((int, float),
        re.compile(f"([0-9]*) *points of displ data equally spaced at *({RE_DECIMAL})", re.IGNORECASE)
    ),
}
# fmt: on

def read_event(read_file, verbosity=0, **kwds):
    """
    Take the name of a CSMIP zip file and extract record data for the event.
    """
    zippath = Path(read_file)
    archive = zipfile.ZipFile(zippath)
    components = []
    motions = defaultdict(QuakeMotion)
    for file in archive.namelist():
        if file.endswith(".v2") or file.endswith(".V2"):
            if verbosity:
                print(file, file=sys.stderr)
            cmp = read_record_v2(file, archive, verbosity=verbosity, **kwds)
            loc = to_key(cmp["location_name"])
            drn = to_key(cmp["component"])
            if drn in motions[loc].components:
                loc += "_alt"
            motions[loc]["key"] = loc
            motions[loc].components[drn] = cmp
    metadata = {}
    return QuakeCollection(motions, **metadata)


def read_record_v2(
    read_file, archive: zipfile.ZipFile = None, 
    verbosity=0,
    summarize=False,
    exclusions=(),
    **kwds
) -> QuakeComponent:
    """
    Read a ground motion record using the CSMIP Volume 2 format
    """
    filename = Path(read_file)
    keys = []
    for x in exclusions:
        for k in HEADER_FIELDS:
            if any(fnmatch.fnmatch(kk,x) for kk in k):
                keys.append(k)
    for k in keys:
        HEADER_FIELDS.pop(k)

    # Parse header fields
    with open_quake(read_file, "r", archive) as f:
        header_data = parse_sequential_fields(f, HEADER_FIELDS)

    header_data.pop("_")

    parse_options = dict(
        delimiter=10,  # fields are 10 chars wide
    )
    # Reopen and parse out data; Note, only the first call
    # provides a skip_header argument as successive reads
    # pick up where the previous left off.
    with open_quake(read_file, "r", archive) as f:
        # 50 integer values spanning 7 lines  between lines 26-32
        int_header = np.genfromtxt(
            f,
            dtype=int,
            skip_header=25,
            max_rows=6,
            delimiter=5,
            ).flatten()
        int_header = np.append(int_header , np.genfromtxt(
            f,
            dtype=int,
            max_rows=1,
            delimiter=5,
            ).flatten()
        )
        assert len(int_header) == 100

        # 100 floating point values on lines 33-45
        real_header = np.genfromtxt(
            f,
            max_rows=45-33,
            delimiter=10,
            ).flatten()
        real_header = np.append(real_header , np.genfromtxt(
            f,
            max_rows=1,
            delimiter=10,
            ).flatten()
        )
        assert len(real_header) == 100
        num_header = _process_numeric_headers_v2(int_header, real_header, header_data)

        if not summarize:
            accel = np.genfromtxt(
                f,
                # skip_header=HEADER_END_LINE + 1,
                skip_header=1,
                max_rows=np.ceil(header_data["accel.shape"]/NUM_COLUMNS) - 1,
                **parse_options,
            ).flatten()
            accel = np.append(accel, np.genfromtxt(f,max_rows=1,**parse_options))
            next(f)
            veloc = np.genfromtxt(
                f, max_rows=np.ceil(header_data["veloc.shape"]/NUM_COLUMNS)-1, **parse_options
            ).flatten()
            veloc = np.append(veloc, np.genfromtxt(f,max_rows=1,**parse_options))
            next(f)
            displ = np.genfromtxt(
                f, max_rows=np.ceil(header_data["displ.shape"]/NUM_COLUMNS)-1, **parse_options
            ).flatten()
            displ = np.append(displ, np.genfromtxt(f,max_rows=1,**parse_options))
        else:
            accel, veloc, displ = [], [], []

    # Extract metadata
    try:
        filter_data = {
            key[16:]: header_data.pop(key)
            for key in [
              "filter.bandpass.point", 
              "filter.bandpass.point.units", 
              "filter.bandpass.limit_low",
              "filter.bandpass.limit_high",
              "filter.bandpass.limit.units"
            ]
        }
    except:
        filter_data = {}
    record_data = {"filters": [{"filter_type": "bandpass",**filter_data}]}
    series_data = defaultdict(dict)
    for key, val in header_data.items():
        typ, k = key.split(".", 1)
        if typ == "record":
            record_data.update({k: val})
        elif typ in ["accel", "veloc", "displ"]:
            series_data[typ].update({k: val})

    record_data["file_name"] = filename.name
    record_data["ihdr"] = int_header
    record_data["rhdr"] = real_header
    return QuakeComponent(
        QuakeSeries(accel, series_data["accel"]),
        QuakeSeries(veloc, series_data["veloc"]),
        QuakeSeries(displ, series_data["displ"]),
        meta=record_data,
    )

def _process_numeric_headers_v2(ihdr, rhdr, txthdr):
    data = {}
    ref_azimuth = ihdr[32 -1]
    rel_orientation = ihdr[27 -1]
    #assert txthdr["veloc.shape"] == ihdr[64 - 1]
    #txthdr["record.earthquake_name"] = txthdr["record.earthquake_name"][:ihdr[29 - 1]+1]

    #assert ihdr[51 -1] == ihdr[52-1]
    #assert ihdr[28 -1] == ihdr[51-1]


FILE_TYPES = {
    "csmip.v1": {"type": QuakeComponent, "read": read_record_v2},
    "csmip.v2": {"type": QuakeComponent, "read": read_record_v2},
    "csmip.v3": {"type": QuakeComponent, "read": read_record_v2, "spec": ""},
    "csmip.zip": {"type": QuakeCollection, "read": read_event},
}


def read_record(read_file, *args):
    file = Path(read_file)
    if file.suffix == ".v2":
        return read_record_v2(file)


def read(read_file, input_format=None):
    # file_type = get_file_type(file,file_type,"csmip")
    # if isinstance(
    pass

