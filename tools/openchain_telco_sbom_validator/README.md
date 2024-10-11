# openchain-telco-sbom-validator

A script to validate SBOMs against version 1.0 of
the [OpenChain Telco SBOM Guide](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md).

# Installation

To install from [PyPI](https://pypi.org/project/openchain-telco-sbom-validator/), issue `pip3 install openchain-telco-sbom-validator`.

# Manual installation

This script is written in Python and uses a `requirements.txt` to list its dependencies. To install Python on an Ubuntu
environment run `sudo apt install python3-pip`.

It is usually a good practice to install Python dependencies to a Python virtual environment. To be able to manage
virtual environments you need to install `venv` with `sudo apt install python3-venv`.

If you do not have a virtual environment you can create it with `python3 -m venv .env`,
if you already have a virtual environment start it with `. .env/bin/activate`.


# Usage

## From command line

```
usage: openchain-telco-sbom-validator [options] input

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

## As a library

The main functionality of the library can be acessed from the `Validator` class of the
`openchain_telco_sbom_validator.validator` package. There are two support packages for building CLI tools around the
validator what is in the `cli` package of the `openchain_telco_sbom_validator` package.

```
# import things

from openchain_telco_sbom_validator import cli
from openchain_telco_sbom_validator import reporter
from openchain_telco_sbom_validator.validator import Validator

def main():
    # Instantiate a validator

    myValidator = Validator()

    # Do validate
    result, problems = myValidator.validate(filePath,          # path to the SPDX file as a string
                                            strict_purl_check, # If strict purl check is needed
                                            strict_url_check)  # if strict URL check is needed

    # Print results in an uniform way

    exitCode = reporter.reportCli(result,        # Result received from the validator
                                  problems,      # List of problems from the validator
                                  nr_of_errors,  # Number of errors to display
                                  input)         # Name of the SPDX file

    # Exit
    sys.exit(exitCode)


```

### Extensibility

#### Command line arguments

It is possible to add additional CLI arguments if needed for example:

```
    myArguments = cli.AdditionalArguments()
    myArguments.addArgument("--test",                    # The actual argument
                            "store_true",                # Option as it is required by argparse
                            "Help description of test")  # Help text to display

    args = cli.parseArguments(myArguments)

    if args.test:
      pass # Do something here
```

#### Additional checks

It is possible to add additional checks both on global and on package level.

```
    # Import in addition of the previous imports
    from openchain_telco_sbom_validator.validator import FunctionRegistry

    myValidator = Validator()

    # Instantiate the function registry
    functions = FunctionRegistry()

    # Register a global check. This will be executed only once for one SBOM
    functions.registerGlobal(checkJustLog)

    # Register a Package chack. This will be executed for every Packages in the SBOM
    functions.registerPackage(checkJustLogPackage)

    result, problems = myValidator.validate(filePath,
                                            strict_purl_check,
                                            strict_url_check,
                                            functions)         # Provide the function registry to the validate function

  # The functions have to be defined
def checkJustLog(problems: Problems, doc: Document): # Signature is important!
    logger = logging.getLogger(__name__)
    logger.debug("Hello world!")

def checkJustLogPackage(problems: Problems, package: Package): # Signature is important!
    logger = logging.getLogger(__name__)
    logger.debug("Hello package world!")


```

# License

This software is Copyright Nokia and is licensed under the Apache 2.0 license.

# Issues and contributions

In case of any issues please create a GitHub issue, while also any contributions are warmly welcome in the form of
GitHub merge requests.
