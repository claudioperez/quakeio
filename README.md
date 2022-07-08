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
[gh-link]: https://github.com/claudioperez/quakeio/compare/v0.1.14...master
[gh-image]: https://img.shields.io/github/commits-since/claudioperez/quakeio/v0.1.14?style=social


