# quake-io

[![PyPI Downloads][pypi-v-image]][pypi-v-link]
[![PyPI Version][pypi-d-image]][pypi-d-link]
![Coverage][cov-img]
<!-- ![Build][build-img] -->
[![Commits since latest release][gh-image]][gh-link]

QuakeIO is a library of utilities for parsing ground motion files. Interfaces are provided for Python, Matlab, and the command line.

## Formats

| Format          | Read      | Write   |
|-----------------|-----------|---------|
|`csmip`          | &#9744;   | &#9744; |
|`PEER.NGA`       | &#9744;   | &#9744; |
|`plain.tsv`      | &#9744;   | &#9744; |
|`plain.csv`      | &#9744;   | &#9744; |
|`mdof`           | &#9744;   | &#9744; |
| SimCenter.Event | &#9744;   | &#9744; |

## Examples

### Command line

```bash
$ quakeio -a rot:30 chan001.v2 -t html
```

Rotate and calculate Husid series.
```bash
$ quakeio -c 'rot:30;husid;' chan001.v2 
```

```bash
$ cat chan001.v2 | quakeio -a rot:30 -f csmip.v2 -t html | pandoc -f html -t pdf
```

```bash
$ cat chan001.v2 \
    | quakeio -a rot:30 -f csmip.v2 -t html -x [*].data \
    | pandoc -f html -t pdf
```


### Library

```python
import quakeio

csmip_event = quakeio.read("event.zip")
csmip_event["channel-01"].accel.plot()
```

```python
csmip_event["chan001"].plot()
```


```python
csmip_event["chan001"].plot_spect()
```

## Command Line Interface

```
usage: quakeio [OPTIONS] [FILE]
Options:
-c/--calculate COMMAND

-a/--apply  

-t/--to FORMAT

-x/--exclude FIELD

-M/--metadata=KEY[:VALUE]

Commands:
  husid;
  scale:SCALE;
  rotate:cs=ANGLE;
  filter:<freq>;
  spect;

Formats:
  html
  csmip[.v1,.v2,.v3]
  nga
```

<!-- Badge links -->
[pypi-d-image]: https://img.shields.io/pypi/dm/quakeio.img
[license-badge]: https://img.shields.io/pypi/l/quakeio.img
[pypi-d-link]: https://pypi.org/project/quakeio
[pypi-v-image]: https://img.shields.io/pypi/v/quakeio.img
[pypi-v-link]: https://pypi.org/project/quakeio
[build-img]: https://github.com/claudioperez/quakeio/actions/workflows/base.yml/badge.svg
[cov-img]: ./etc/coverage/cov.svg
[gh-link]: https://github.com/claudioperez/quakeio/compare/0.0.0...master
[gh-image]: https://img.shields.io/github/commits-since/claudioperez/quakeio/0.0.0?style=social

