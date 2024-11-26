from openchain_telco_sbom_validator import validator

def test_ok_json():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-01.spdx.json")
    assert len(problems) == 0
    assert result == True

def test_ok():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-02.spdx")
    assert len(problems) == 0
    assert result == True
