# Python PGP Check

A quick python CLI tool to verify file PGP hashes


### Installation and usage

Install it with python pip using 

``` bash
    pip install python-pgp-check
```

Use it like this

```bash
    python-pgp-check <file_path> <expected_hash> 
``` 

### Specifying Hash Algorithm

By default, SHA-256 is used. To use a different algorithm:

```bash
 python-pgp-check <file_path> <expected_hash> --algorithm <algorithm> 
 ``` 

