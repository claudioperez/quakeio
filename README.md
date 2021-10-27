# quake-io

[![PyPI Downloads][pypi-v-image]][pypi-v-link]
[![PyPI Version][pypi-d-image]][pypi-d-link]
![][cov-img]
<!-- ![Build][build-img] -->
[![Commits since latest release][gh-image]][gh-link]

QuakeIO is a library of utilities for parsing ground motion files. Interfaces are provided for Python, Matlab, and the command line.

- [Install](#install)
- [Formats](#formats)
- [Python API](#Python-API)


## Formats

| Format          | Read      | Write   |  Reference              |
|-----------------|-----------|---------|-------------------------|
|`[quakeio.]json` | &#9745;   | &#9745; | [schema][record-schema] |
|`csmip`          | &#9744;   | &#9744; |                         |
|`csmip.v2`       | &#9745;   | &#9744; | [CSMIP][CSMIP]          |
|`eqsig`          | &#9745;   | &#9745; | [eqsig][EQSIG]          |
|`PEER.NGA`       | &#9745;   | &#9744; |                         |
|`plain.tsv`      | &#9744;   | &#9744; |                         |
|`opensees`       | &#9744;   | &#9745; |                         |
|`plain.csv`      | &#9744;   | &#9744; |                         |
|`mdof`           | &#9744;   | &#9744; |                         |
| SimCenter.Event | &#9744;   | &#9744; |                         |

## Install

Run the following command:

```shell
pip install quakeio
```


## Python API


```python
import quakeio

# Read event
csmip_event = quakeio.read("event.zip")

## Extract record and rotate
record = rec = csmip_event["bent_4_north_column_grnd_level"]
angle = 21/7
record.rotate(angle)

## Extract rotated series
series = record['tran'].accel

# Write output
quakeio.write("out.txt", series, write_format="opensees")
```


## Command Line Interface

```
usage: quakeio FILE [-f FORMAT] [-t FORMAT]

Options:
-c/--calculate COMMAND
 
-f/--from FORMAT
-t/--to   FORMAT
```

```bash
$ quakeio chan001.v2 --from csmip.v2 --to opensees
```

<!--
Rotate and calculate Husid series.
```bash
$ quakeio -c 'rot:30;husid;' chan001.v2 
```
-->

```bash
$ cat chan001.v2 | quakeio -f csmip.v2 -t html | pandoc -f html -t pdf
```

```bash
$ cat chan001.v2 \
    | quakeio -a rot:30 -f csmip.v2 -t html -x [*].data \
    | pandoc -f html -t pdf
```

## MATLAB Interface

```matlab
Motion = quakeIO.read('csmip.zip')
```



<!-- Reference links -->
[EQSIG]: https://github.com/eng-tools/eqsig
[CSMIP]: https://www.conservation.ca.gov/cgs/Documents/Program-SMIP/Reports/Other/OSMS_85-03.pdf
[record-schema]: https://raw.githubusercontent.com/claudioperez/quakeio/master/etc/schemas/record.schema.json

<!-- Badge links -->
[pypi-d-image]: https://img.shields.io/pypi/dm/quakeio.svg
[license-badge]: https://img.shields.io/pypi/l/quakeio.svg
[pypi-d-link]: https://pypi.org/project/quakeio
[pypi-v-image]: https://img.shields.io/pypi/v/quakeio.svg
[pypi-v-link]: https://pypi.org/project/quakeio
[build-img]: https://github.com/claudioperez/quakeio/actions/workflows/base.yml/badge.svg
[cov-img]: https://raw.githubusercontent.com/claudioperez/quakeio/master/etc/coverage/cov.svg
[gh-link]: https://github.com/claudioperez/quakeio/compare/0.0.5...master
[gh-image]: https://img.shields.io/github/commits-since/claudioperez/quakeio/0.0.5?style=social


