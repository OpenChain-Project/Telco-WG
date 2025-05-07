#!/bin/python3

# © 2024-2025 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

from prettytable import PrettyTable
import shutil
from importlib.metadata import version, PackageNotFoundError

def reportCli(result, problems, nr_of_errors, input, guide_version, strict):
    if not result:
        if problems:
            if nr_of_errors:
                problems = problems[0:int(nr_of_errors)]

        resultTable = PrettyTable(align = "l")
        resultTable.padding_width = 1

        # TODO: now Error type and SPDX ID uses more space than Package name and Reason, this should be vice versa
        width = shutil.get_terminal_size().columns

        if problems.print_file:
            resultTable.field_names = ["#", "Error type", "File", "SPDX ID", "Package name", "Reason"]
            resultTable._max_width = {"#": 5,
                                        "Error type": int((width - 4)/6),
                                        "File:": int((width - 4)/6),
                                        "SPDX ID": int((width - 4)/6),
                                        "Package name": int((width - 4)/3),
                                        "Reason": int((width - 4)/3)}
        else:
            resultTable.field_names = ["#", "Error type", "SPDX ID", "Package name", "Reason"]
            resultTable._max_width = {"#": 4,
                                        "Error type": int((width - 4)/6),
                                        "SPDX ID": int((width - 4)/6),
                                        "Package name": int((width - 4)/3),
                                        "Reason": int((width - 4)/3)}

        i = 0
        for problem in problems:
            i = i + 1
            if problems.print_file:
                resultTable.add_row([i, problem.ErrorType, problem.file, problem.SPDX_ID, problem.PackageName, problem.Reason], divider=True)
            else:
                resultTable.add_row([i, problem.ErrorType, problem.SPDX_ID, problem.PackageName, problem.Reason], divider=True)

        print(resultTable)
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

def reportVersion():
    try:
        __version__ = version("openchain-telco-sbom-validator")
    except PackageNotFoundError:
        __version__ = "unknown"
    print(f"OpenChain Telco SBOM Validator version {__version__}")
