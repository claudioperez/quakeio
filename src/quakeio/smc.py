"""
https://escweb.wr.usgs.gov/nsmp-data/smcfmt.html
"""
import sys
import zipfile
from pathlib import Path
from collections import defaultdict

import numpy as np

from .utils.parseutils import open_quake

from .core import (
    QuakeCollection,
    QuakeMotion,
    QuakeComponent,
    QuakeSeries,
)

def _read_smc(read_file, archive = None, summarize=False):

    NUM_COLUMNS = 8
    with open_quake(read_file, "r", archive) as f:
        # First 11 lines
        txt_header = [next(f) for _ in range(11)]

        # 48 integer values spanning 6 lines
        int_header = np.genfromtxt(
            f,
            dtype=int,
            max_rows=5,
            ).flatten()
        int_header = np.append(int_header , np.genfromtxt(
            f,
            dtype=int,
            max_rows=1,
            ).flatten()
        )
        assert len(int_header) == 48

        # Value representing "undefined" or "null" in the integer header.
        int_null = int_header[0]

        real_header = [next(f) for _ in range(10)]

#       real_header = np.genfromtxt(
#           f,
#           max_rows= 10,
#           delimiter=10,
#       ).flatten()

        num_comment_lines = int_header[15]
        len_accel = int_header[16]
        comments = [next(f) for _ in range(num_comment_lines)]

        if not summarize:
            data = np.genfromtxt(
                f,
                delimiter=10,
                # skip_header=HEADER_END_LINE + 1,
                max_rows=np.ceil(len_accel/NUM_COLUMNS) - 1,
            ).flatten()
            data = np.append(data, np.genfromtxt(f,max_rows=1))
        else:
            data = []

    return txt_header, int_header, real_header, data

def read_series(
    read_file,
    archive: zipfile.ZipFile = None,
    verbosity: int  = 0,
    summarize: bool =False,
    exclusions: tuple = (),
    **kwds
) -> QuakeSeries:

        txt_header, int_header, real_header, data = _read_smc(read_file, archive, summarize=summarize)

        motion_data = {
            "component": int_header[12],
            "location_name": str(txt_header[5][10:]).split("component")[0]
        }

        return QuakeSeries(data, meta={"type": str(txt_header[0])}), motion_data



def read_event(read_file, verbosity=0, summarize=False, **kwds)->QuakeCollection:
    """
    """

    components = defaultdict(dict)
    zippath    = Path(read_file)
    archive    = zipfile.ZipFile(zippath)
    file_data = defaultdict(lambda : defaultdict(dict))


    # Loop over files in the zipped archive
    for file in archive.namelist():

        # Disregard any files that are not .smc
        if not file.endswith(".smc"):
            continue

        # Optional info logging
        if verbosity > 2:
            print(f"\t\t{file}", file=sys.stderr)

        series, motion_data = read_series(file, archive, verbosity=verbosity,
                                          summarize=summarize, **kwds)

        stype = file.split("_")[-1]
        stype = {
            "a.smc": "accel",
            "d.smc": "displ",
            "v.smc": "veloc",
        }[stype]

        component = file_data[motion_data["location_name"]][motion_data["component"]]
        if stype in component and "corrected" in component[stype]["type"].lower():
            # If we already have the corrected values, pass
            pass
        else:
            component[stype] = series


    date = None
    motions = {
            k: QuakeMotion({
                dir: QuakeComponent(
                       component.get("accel", None),
                       component.get("veloc", None),
                       component.get("displ", None),
                    meta=dict(component=dir))
                for dir,component in motion.items()
            }, dict(location_name=k))
            for k, motion in file_data.items()
    }

    # Collect some other information from the first file (component)
    first_motion    = list(motions.values())[0]
    first_component = list(first_motion.components.values())[0]


    metadata = {
        "file_name": str(read_file),
        "station_name":      first_component.get("station_name", "NA"),
        "station_coord":     first_component.get("station.coord", "NA"),
        "record_identifier": first_component.get("record_identifier", "NA"),
        "station_number":    first_component.get("station.no", "NA")
    }
    return QuakeCollection(motions, event_date=date, meta=metadata)



