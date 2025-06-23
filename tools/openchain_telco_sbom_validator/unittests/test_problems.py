from openchain_telco_sbom_validator.validator import Problem, Problems

def test_get_sorted_by_scope():

    # Create a Problems instance
    problems = Problems()

    # Add Problem instances with different scopes
    problems.add(Problem("ErrorType1", "SPDX1", "Package1", "Reason1", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_WARNING))
    problems.add(Problem("ErrorType2", "SPDX2", "Package2", "Reason2", Problem.SCOPE_SPDX, Problem.SEVERITY_ERROR))
    problems.add(Problem("ErrorType3", "SPDX3", "Package3", "Reason3", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR))

    # Get sorted iterator
    sorted_problems = list(problems.get_sorted_by_scope())

    # Assert the order based on scope
    assert sorted_problems[0].scope == Problem.SCOPE_OPEN_CHAIN
    assert sorted_problems[1].scope == Problem.SCOPE_OPEN_CHAIN
    assert sorted_problems[2].scope == Problem.SCOPE_SPDX

    # Optionally, assert the specific order of objects if needed
    assert sorted_problems[0].SPDX_ID == "SPDX1"
    assert sorted_problems[1].SPDX_ID == "SPDX3"
    assert sorted_problems[2].SPDX_ID == "SPDX2"

def test_get_errors():
    # Create a Problems instance
    problems = Problems()

    # Add Problem instances with different scopes
    problems.add(Problem("ErrorType1", "SPDX1", "Package1", "Reason1", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_WARNING))
    problems.add(Problem("ErrorType2", "SPDX2", "Package2", "Reason2", Problem.SCOPE_SPDX, Problem.SEVERITY_ERROR))
    problems.add(Problem("ErrorType3", "SPDX3", "Package3", "Reason3", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR))

    errors = problems.get_errors()
    assert len(errors) == 2
    assert errors[0].SPDX_ID == "SPDX2"
    assert errors[1].SPDX_ID == "SPDX3"

def test_get_warnings():
    # Create a Problems instance
    problems = Problems()

    # Add Problem instances with different scopes
    problems.add(Problem("ErrorType1", "SPDX1", "Package1", "Reason1", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_WARNING))
    problems.add(Problem("ErrorType2", "SPDX2", "Package2", "Reason2", Problem.SCOPE_SPDX, Problem.SEVERITY_ERROR))
    problems.add(Problem("ErrorType3", "SPDX3", "Package3", "Reason3", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR))

    errors = problems.get_warnings()
    assert len(errors) == 1
    assert errors[0].SPDX_ID == "SPDX1"
     
def test_bool_operator_errors():
    # Create a Problems instance
    problems = Problems()

    problems.add(Problem("ErrorType1", "SPDX1", "Package1", "Reason1", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_WARNING))
    assert not problems

    problems.add(Problem("ErrorType3", "SPDX3", "Package3", "Reason3", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR))
    assert problems