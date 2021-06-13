import re

import numpy as np

RE_TIME_STEP = re.compile("DT=\s+(.*)SEC")


def parse_nga(file_name, meta=False):
    with open(file_name, "r") as f:
        header = [next(f) for _ in range(4)]
    dt = float(RE_TIME_STEP.search(header[-1]).group(1).strip())
    accel = np.genfromtext(file_name, skip_header=4, skip_footer=1).flatten()
