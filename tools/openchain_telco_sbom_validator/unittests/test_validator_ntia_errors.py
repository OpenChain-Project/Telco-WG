from openchain_telco_sbom_validator.validator import Validator

def test_nok_empty_name():
    validator = Validator()
    result, problems = validator.validate("sboms/unittest-sbom-05.spdx")
    assert len(problems) == 2
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a name"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-796a192b709a2a2b"
    assert problems[1].ErrorType == "NTIA validation error"
    assert problems[1].Reason == "Package without a version"
    assert problems[1].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-796a192b709a2a2b"
    assert result == False

def test_nok_no_version():
    validator = Validator()
    result, problems = validator.validate("sboms/unittest-sbom-06.spdx")
    assert isinstance(validator, Validator)
    assert False
    assert len(problems) == 1
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a name"
    assert result == False
