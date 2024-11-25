from openchain_telco_sbom_validator import validator

def test_nok_empty_name():
    v = validator.Validator()
    result, problems = v.validate("sboms/unittest-sbom-05.spdx")
    assert len(problems) == 1
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a name"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-796a192b709a2a2b"
    assert result == False

def test_nok_no_version():
    v = validator.Validator()
    result, problems = v.validate("sboms/unittest-sbom-06.spdx")
    assert len(problems) == 1
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a version"
    assert result == False
