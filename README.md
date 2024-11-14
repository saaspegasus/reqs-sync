# reqs-sync

[![PyPI](https://img.shields.io/pypi/v/reqs-sync.svg)](https://pypi.org/project/reqs-sync/)
[![Changelog](https://img.shields.io/github/v/release/saaspegasus/reqs-sync?include_prereleases&label=changelog)](https://github.com/saaspegasus/reqs-sync/releases)
[![Tests](https://github.com/saaspegasus/reqs-sync/actions/workflows/test.yml/badge.svg)](https://github.com/saaspegasus/reqs-sync/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/saaspegasus/reqs-sync/blob/master/LICENSE)

null

## Installation

Install this tool using `pip`:
```bash
pip install reqs-sync
```
## Usage

For help, run:
```bash
reqs-sync --help
```
You can also use:
```bash
python -m reqs_sync --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd reqs-sync
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
