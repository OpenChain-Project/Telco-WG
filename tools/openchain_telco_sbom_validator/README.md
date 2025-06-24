# openchain-telco-sbom-validator

A script to validate SBOMs against
the [OpenChain Telco SBOM Guide](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md).

What is new in version 0.3.1:
* new option `--noassertion` will list fields that have value NOASSERTION,
* implement the strict mode for tool name and version (presence of "-"),
* the option `--strict-url-check` now checks the PackageDownloadLocation instead of the PackageHomePage.

What is new in version 0.3.0:
* you can validate recursively SBOMs linked by SPDX Relationships,
* you can validate against version 1.0 or 1.1 of the Guide (default is 1.1),
* you can check only MANDATORY fields or MANDATORY and RECOMMENDED fields (default is MANDATORY only).

# Installation

To install from [PyPI](https://pypi.org/project/openchain-telco-sbom-validator/), issue `pip3 install openchain-telco-sbom-validator`
or `pipx install openchain-telco-sbom-validator`.

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
usage: openchain-telco-sbom-validator [-h] [-v] [--debug] [--nr-of-errors NR_OF_ERRORS] [--strict-purl-check]
[--strict-url-check] [--strict] [-r] [--reference-logic REFERENCE_LOGIC] [--guide-version {1.0,1.1}] [--noassertion] [input]

A script to validate an SPDX file against the OpenChain Telco SBOM Guide (version 1.0 or 1.1).

positional arguments:
  input                 The input SPDX file.

options:
  -h, --help            Shows this help message and exits.
  -v, --version         Prints version and exits.
  --debug               Prints debug logs.
  --nr-of-errors NR_OF_ERRORS
                        Sets a limit on the number of errors displayed.
  --strict-purl-check   Runs a strict check on the given purls. The default behaviour is to run a non-strict purl check
                        meaning that it is not checked if the purl is translating to a downloadable URL.
  --strict-url-check    Runs a strict check on the URLs of the PackageHomepages. Strict check means that the validator
                        checks also if the given URL can be accessed. The default behaviour is to run a non-strict URL
                        check, meaning that it is not checked if the URL points to a valid page. Strict URL check
                        requires access to the internet and takes some time.
  --strict              Checks for both MANDATORY and RECOMMENDED fields. Default is to check MANDATORY fields only.
  -r, --recursive       Validate recursively. Same as “--reference-logic checksum-all”.
  --reference-logic REFERENCE_LOGIC
                        Defines the logic how the referenced files are accessible. If not added, the referenced files
                        will not be investigated. Built-in supported logics are “none” (no linked files are
                        investigated), “checksum-all” (externalrefs are identified by their checksum), “yocto-all”
                        (all externalrefs are investigated) and “yocto-contains-only” (only those files are investigated
                        which are in CONTAINS relationships). It is possible to register more reference logics in
                        library mode.
  --guide-version {1.0,1.1}
                        Defines the version of the OpenChain Telco SBOM Guide to use as a basis for the
                        validation. Possible values are 1.0 and 1.1, default value is 1.1.
  --noassertion         Lists fields with value NOASSERTION.

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

#### Referring logics

Referring SPDX files is based on URLs what assues that all the SBOMs are always public. This is not always the case,
therefore the validator provides a possibility to resolve the references in a local disk. This resolution can be
different depending on the tool generated the SBOMs. It is possible to register referring logics to the validator using
its `addReferringLogics(name, function)` method the function will get a `Document` from `spdx_tools.spdx.model.document`
what is the parsed SPDX model of the currently validated document and a string with the location of the currently
validated document. The function is expected to return a list of file locations with all the referred SPDX files.
Each of these files will be validated as well. The referring logic can be triggered by adding the name of the function
to the `referringLogic` parameter of the `validate()` function of the `Validator` class.

# License

This software is Copyright Nokia and is licensed under the Apache 2.0 license.

# Issues and contributions

In case of any issues please create a GitHub issue, while also any contributions are warmly welcome in the form of
GitHub merge requests.
