from openchain_telco_sbom_validator import validator

def test_nok_supplier_missing():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-11.spdx")
    print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a package supplier"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-Nosupplier-Nochecksum"
    assert problems[0].PackageName == "Nosupplier-Nochecksum-libldap-2.4-2"

def test_nok_purls():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", strict_url_check=True)
    print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "Invalid field in Package"
    assert problems[0].Reason == "PackageDownloadLocation field points to a nonexisting page (https://www.not-openldap.org/)"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-badpurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[0].PackageName == "badpurl-libldap-2.4-2"
