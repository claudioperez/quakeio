from pathlib import Path

import quakeio

csmip_dir = Path("dat/58658_007_20210426_10.09.54.P")

quakeio.read(csmip_dir / "chan001.v2")
