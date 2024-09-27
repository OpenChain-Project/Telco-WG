from prettytable import PrettyTable
import shutil

def reportCli(result, problems, nr_of_errors, input):
    if not result:
        if problems:
            if nr_of_errors:
                problems = problems[0:int(nr_of_errors)]

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
        print(f"The SPDX file {input} is not compliant with the OpenChain Telco SBOM Guide")
        return 1
    else:
        print(f"The SPDX file {input} is compliant with the OpenChain Telco SBOM Guide")
        return 0
