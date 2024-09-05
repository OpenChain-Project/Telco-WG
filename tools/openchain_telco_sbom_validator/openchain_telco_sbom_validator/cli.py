#!/bin/python3

# © 2024 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
from prettytable import PrettyTable
import shutil
import sys
from  validator import validate



def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='A script to validate an SPDX file against the OpenChain Telco SBOM Guide.')
    # TODO: This should go in without any parameter.
    parser.add_argument('--debug', action="store_true",
                        help='Print debug logs.')
    parser.add_argument('--nr-of-errors',
                        help='Sets a limit on the number of errors displayed')
    parser.add_argument('input',
                        help='The input SPDX file.')
    parser.add_argument('--strict-purl-check', action="store_true",
                        help='Runs a strict check on the given purls. The default behaviour is to run a non strict purl'
                        'check what means that it is not checked if the purl is translating to a downloadable url.')
    parser.add_argument('--strict-url-check', action="store_true",
                        help='Runs a strict check on the URLs of the PackageHomepages. Strict check means that the'
                        ' validator checks also if the given URL can be accessed. The default behaviour is to run a non'
                        ' strict URL check what means that it is not checked if the URL points to a valid page. Strict'
                        'URL check requires access to the internet and takes some time.')

    args = parser.parse_args()

    # print(args)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging is ON")
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

    logger.debug("Start parsing")

    filePath = str(args.input)

    result, problems = validate(filePath, args.strict_purl_check, args.strict_url_check)

    if not result:
        if problems:
            if args.nr_of_errors:
                problems = problems[0:int(args.nr_of_errors)]

        resultTable = PrettyTable(align = "l")
        resultTable.padding_width = 1
        resultTable.field_names = ["#", "Error type", "SPDX ID", "Package name", "Reason"]

        # TODO: now Error type and SPDX ID uses more space than Package name and Reason, this should be vice versa
        width = shutil.get_terminal_size().columns
        resultTable._max_width = {"#": 4,
                                  "Error type": int((width - 4)/6),
                                  "SPDX ID": int((width - 4)/6),
                                  "Package name": int((width - 4)/3),
                                  "Reason": int((width - 4)/3)}
        i = 0
        for problem in problems:
            i = i + 1
            resultTable.add_row([i, problem.ErrorType, problem.SPDX_ID, problem.PackageName, problem.Reason], divider=True)

        print(resultTable)
        print(f"The SPDX file {args.input} is not compliant with the OpenChain Telco SBOM Guide")
        sys.exit(1)
    else:
        print(f"The SPDX file {args.input} is compliant with the OpenChain Telco SBOM Guide")
        sys.exit(0)

if __name__ == "__main__":
    main()
