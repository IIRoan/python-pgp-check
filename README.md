# Python PGP Check

[![PyPI Version](https://img.shields.io/pypi/v/python-pgp-check)](https://pypi.org/project/python-pgp-check/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/python-pgp-check)](https://pypi.org/project/python-pgp-check/)

[![License](https://img.shields.io/pypi/l/python-pgp-check)](https://pypi.org/project/python-pgp-check/)
[![Format](https://img.shields.io/pypi/format/python-pgp-check)](https://pypi.org/project/python-pgp-check/)
[![Implementation](https://img.shields.io/pypi/implementation/python-pgp-check)](https://pypi.org/project/python-pgp-check/)
[![Package Size](https://img.shields.io/github/repo-size/iiroan/python-pgp-check)](https://github.com/iiroan/python-pgp-check)

A quick python CLI tool to verify file PGP hashes


### Installation and usage

Install it with python pip using 

``` bash
pip install python-pgp-check
```

### Usage
Calculate Hash

to calculate the hash of a file:
```bash
python-pgp-check <file_path>
``` 

Verify Hash

To verify a file against an expected hash:
```bash
python-pgp-check <file_path> <expected_hash>
```

Specifying Hash Algorithm

By default, SHA-256 is used. To use a different algorithm:

```bash
python-pgp-check <file_path> [<expected_hash>] --algorithm <algorithm>
```

Supported algorithms: md5, sha1, sha256, sha512

### Examples

Calculate SHA-256 hash:
```bash
python-pgp-check /path/to/file
```
Verify file with SHA-256 hash:
```bash
python-pgp-check /path/to/file 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

Calculate MD5 hash:
```bash
python-pgp-check /path/to/file --algorithm md5
```
Verify file with SHA-512 hash:
```bash
python-pgp-check /path/to/file 3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2 --algorithm sha512
```



### Dev Setup

1. Create a virtual environment:
```bash
# On Windows
python -m venv venv

# On macOS/Linux
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

## Installation Options

### Option 1: Development Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the CLI directly for testing:
```bash
python src/pgp_check/cli.py
```

### Option 2: Package Installation

1. Install the package in editable mode:
```bash
pip install -e .
```

## Verification

Test the it installed correctly:
```bash
# If installed with Option 2
python-pgp-check --version
```

## Notes
- Always ensure your virtual environment is activated before running commands (you should see `(venv)` in your terminal prompt)
- Use `deactivate` to exit the virtual environment when done
- If you encounter permission errors, you may need to use `sudo` (Linux/macOS) or run as administrator (Windows)
