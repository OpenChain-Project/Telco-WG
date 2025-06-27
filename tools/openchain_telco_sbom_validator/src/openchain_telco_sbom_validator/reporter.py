#!/bin/python3

# © 2024-2025 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import logging
import shutil
from importlib.metadata import version, PackageNotFoundError
from prettytable import PrettyTable

logger = logging.getLogger(__name__)
logger.propagate = True

def reportCli(result, problems, nr_of_errors, input, guide_version, strict, noassertion, strict_purl_check, strict_url_check):
    if problems == None:
        print("Internal error.")
        return 2
    
    if len(problems):

        errors = problems.get_errors()
        warnings = problems.get_warnings()
        noasserts = problems.get_noasserts()
        incorrect_purls = problems.get_incorrect_purls()
        incorrect_urls = problems.get_incorrect_urls()

        if nr_of_errors:
            errors = errors[0:int(nr_of_errors)]
            noasserts = noasserts[0:int(nr_of_errors)]
            incorrect_purls = incorrect_purls[0:int(nr_of_errors)]
            incorrect_urls = incorrect_urls[0:int(nr_of_errors)]
        logger.debug(f"Problems: {problems}, Errors {errors}, Warnings {warnings}")

        if len(errors):
            printTable(errors, problems.print_file)

        if noassertion:
            if len(warnings):
                print("Fields with NOASSERTION:")
                printTable(warnings, problems.print_file)
            else:
                print("There are no fields with NOASSERTION.")

        if strict_purl_check:
            if len(incorrect_purls):
                print("Fields with purl that cannot be converted to a downloadable URL:")
                printTable(incorrect_purls, problems.print_file)

        if strict_url_check:
            if len(incorrect_urls):
                print("PackageDownloadLocation field points to a nonexisting page:")
                printTable(incorrect_urls, problems.print_file)

    if not result:
        if len(problems.checked_files) == 1:
            if strict:
                print(f"The SPDX file {input} is not compliant with the OpenChain Telco SBOM Guide version {guide_version} in strict mode (with RECOMMENDED also)")
            else:
                print(f"The SPDX file {input} is not compliant with the OpenChain Telco SBOM Guide version {guide_version}")
        else:
            if strict:
                print(f"One or more of the SPDX files {problems.get_files_as_string()} are not compliant with the OpenChain Telco SBOM Guide version {guide_version} in strict mode (with RECOMMENDED also)")
            else:
                print(f"One or more of the SPDX files {problems.get_files_as_string()} are not compliant with the OpenChain Telco SBOM Guide version {guide_version}")
        return 1
    else:
        if len(problems.checked_files) == 1:
            if strict:
                print(f"The SPDX file {input} is compliant with the OpenChain Telco SBOM Guide version {guide_version} in strict mode (with RECOMMENDED also)")
            else:
                print(f"The SPDX file {input} is compliant with the OpenChain Telco SBOM Guide version {guide_version}")
        else:
            if strict:
                print(f"All of the SPDX files {problems.get_files_as_string()} are compliant with the OpenChain Telco SBOM Guide version {guide_version} in strict mode (with RECOMMENDED also)")
            else:
                print(f"All of the SPDX files {problems.get_files_as_string()} are compliant with the OpenChain Telco SBOM Guide version {guide_version}")
        return 0

def printTable(problems, print_file):
    # TODO: now Error type and SPDX ID uses more space than Package name and Reason, this should be vice versa
    width = shutil.get_terminal_size().columns
    table = PrettyTable(align = "l")
    table.padding_width = 1

    if print_file:
        table.field_names = ["#", "Error type (Scope)", "File", "SPDX ID", "Package name", "Reason"]
        table._max_width = {"#": 5,
                                    "Error type": int((width - 4)/6),
                                    "File:": int((width - 4)/6),
                                    "SPDX ID": int((width - 4)/6),
                                    "Package name": int((width - 4)/3),
                                    "Reason": int((width - 4)/3)}
    else:
        table.field_names = ["#", "Error type (Scope)", "SPDX ID", "Package name", "Reason"]
        table._max_width = {"#": 4,
                                    "Error type": int((width - 4)/6),
                                    "SPDX ID": int((width - 4)/6),
                                    "Package name": int((width - 4)/3),
                                    "Reason": int((width - 4)/3)}
    i = 0
    for problem in problems:
        i = i + 1
        if print_file:
            table.add_row([i, f"{problem.ErrorType} ({problem.scope})", problem.file, problem.SPDX_ID, problem.PackageName, problem.Reason], divider=True)
        else:
            table.add_row([i, f"{problem.ErrorType} ({problem.scope})", problem.SPDX_ID, problem.PackageName, problem.Reason], divider=True)
    print(table)

def reportVersion():
    try:
        __version__ = version("openchain-telco-sbom-validator")
    except PackageNotFoundError:
        __version__ = "unknown"
    print(f"OpenChain Telco SBOM Validator version {__version__}")
