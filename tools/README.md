# openchain-telco-sbom-validator

A script to validate SBOM-s against the OpenChain Telco SBOM Guide

# Usage

```
usage: python3 nokia-sbom-validator.py [options] input

positional arguments:
  input                 The input SPDX file.

options:
  -h, --help            Shows this help message and exits.
  --debug               Prints debug logs.
  --nr-of-errors NR_OF_ERRORS
                        Sets a limit on the number of errors displayed.
  --strict-purl-check   Runs a strict check on the given purls. The default behaviour is to run a non strict purl
                        check what means that it is not checked if the purl is translating to a downloadable URL.
  --strict-url-check    Runs a strict check on the URLs of the PackageHomepages. Strict check means that the
                        validator checks also if the given URL can be accessed. The default behaviour is to run a non
                        strict URL check what means that it is not checked if the URL points to a valid page. Strict
                        URL check requires access to the internet and takes some time.')
```


# Installation of prerequisities

This script is written in python and uses a requirements.txt to list its dependencies. To install python on an Ubuntu
environment run `sudo apt install python3-pip`.

It is usually a good practice to install Python dependencies to a Python virtual environment. To be able to manage
virtual environments you need to install `venv` with `sudo apt install python3-venv`.

If you do not have a virtual environment yet cretate it with `python3 -m venv .env` and install the dependencies with
`pip3 install -r requirements.txt`, if you already have a virtual environment start it with `. .env/bin/activate`.

# License

This software is Copyright Nokia and is licensed under the Apache 2.0 license.

# Issues and contributions

In case of any issues please create a GitHub issue, while also any contributions are warmly welcome in the form of
GitHub merge requests.
