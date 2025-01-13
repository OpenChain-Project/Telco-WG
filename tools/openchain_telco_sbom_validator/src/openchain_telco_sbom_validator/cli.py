#!/bin/python3

# © 2024 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import sys

from openchain_telco_sbom_validator.validator import Validator
from openchain_telco_sbom_validator.reporter import reportCli,reportVersion

logger = logging.getLogger(__name__)
logger.propagate = True

def main():
    try:
        args = parseArguments()

        logLevel = ""
        if args.debug:
            logLevel = logging.DEBUG
            logger.debug("Debug logging is ON")
        else:
            logLevel = logging.INFO
        
        logging.basicConfig(
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logLevel, 
            handlers=[
                logging.FileHandler("log.log"),  # Write logs to a file
                logging.StreamHandler()
            ])

        if args.version:
            reportVersion()
            sys.exit(0)
        
        logger.debug("Start parsing.")

        filePath = str(args.input)
        validator = Validator()

        reference_logic = args.reference_logic
        if None == args.reference_logic:
            reference_logic = "none"
        
        result, problems = validator.validate(filePath,
                                            args.strict_purl_check,
                                            args.strict_url_check,
                                            referringLogic=reference_logic)

        exitCode = reportCli(result, problems, args.nr_of_errors, args.input)
        sys.exit(exitCode)
    except KeyboardInterrupt:
        print(" Ctrl-C pressed. Terminating...")
        sys.exit(2) 

class Argument:
    def __init__(self, argument, action, help):
        self.argument = argument
        self.action = action
        self.help = help

    def __srt__(self):
        return f"argument={self.argument}, action={self.action}, help={self.help}"

class AdditionalArguments:
    def __init__(self):
        self.items  = []

    def addArgument(self, argument, action, help):
        item = Argument(argument, action, help)
        self.items.append(item)
        return self
    
    def __iter__(self):
        return iter(self.items)
    
    def __getitem__(self, index):
        return self.items[index]
    
def parseArguments(additionalArguments: AdditionalArguments = AdditionalArguments()):
    parser = argparse.ArgumentParser(description='A script to validate an SPDX file against version 1 of the OpenChain Telco SBOM Guide.')
    # TODO: This should go in without any parameter.
    parser.add_argument('--debug', action="store_true",
                        help='Prints debug logs.', 
                        required=False)
    parser.add_argument('--nr-of-errors',
                        help='Sets a limit on the number of errors displayed.')
    parser.add_argument('input',
                        help='The input SPDX file.',
                        nargs="?")
    parser.add_argument('--strict-purl-check', action="store_true",
                        help='Runs a strict check on the given purls. The default behaviour is to'
                        ' run a non-strict purl check meaning that it is not checked if the'
                        ' purl is translating to a downloadable URL.')
    parser.add_argument('--strict-url-check', action="store_true",
                        help='Runs a strict check on the URLs of the PackageHomepages. Strict check'
                        ' means that the validator checks also if the given URL can be accessed.'
                        ' The default behaviour is to run a non-strict URL check, meaning that'
                        ' it is not checked if the URL points to a valid page. Strict URL check'
                        ' requires access to the internet and takes some time.')
    parser.add_argument('--reference-logic',
                        help='Defines the logic how the referenced files are accessible. If not'
                        ' added, the referenced files will not be investigated.'
                        ' Built-in supported logics are “none” (no linked files are investigated),'
                        ' “yocto-all” (all externalrefs are investigated) and'
                        ' “yocto-contains-only” (only those files are investigated which are in'
                        ' CONTAIN relationships). It is possible to register more reference'
                        ' logics in library mode')
    parser.add_argument('--version', action="store_true",
                        help='Prints version and exits.', 
                        required=False)

    for argument in additionalArguments:
        logger.debug(f"Adding additional argument {argument}")
        parser.add_argument(argument.argument, action=argument.action, help=argument.help)

    args = parser.parse_args()

    if not args.version:
        if not args.input:
            logger.error("ERROR! Input is a mandatory parameter.")
            sys.exit(2)
        else:
            logger.info("Input file is " + args.input)
            # TODO: Check if the file exist.

    if args.nr_of_errors:
        if not args.nr_of_errors.isnumeric():
            logger.error(f"nr-of-errors must be a number and not {args.nr_of_errors}")
            sys.exit(1)
    if args.strict_purl_check:
        logger.info("Running strict checks for purls, what means that it is tested if the purls can be translated to a downloadable url.")
    if args.strict_url_check:
        logger.info("Running strict checks for URL, what means that it is tested if the PackageHomePage fields are pointing to real pages.")

    return args



if __name__ == "__main__":
    main()
