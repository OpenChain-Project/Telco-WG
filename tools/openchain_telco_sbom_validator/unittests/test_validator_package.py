from openchain_telco_sbom_validator import validator

def test_nok_creater_comment_missing():
    v = validator.Validator()    
    result, problems = v.validate(filePath = "sboms/unittest-sbom-11.spdx")
    assert result == False
    assert len(problems) == 2
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a package supplier or package originator"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-Nosupplier-Nochecksum"
    assert problems[0].PackageName == "Nosupplier-Nochecksum-libldap-2.4-2"
    assert problems[1].ErrorType == "Missing mandatory field from Package"
    assert problems[1].Reason == "Checksum field is missing"
    assert problems[1].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-Nosupplier-Nochecksum"
    assert problems[1].PackageName == "Nosupplier-Nochecksum-libldap-2.4-2"

def test_nok_purls():
    v = validator.Validator()    
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", strict_purl_check=True, strict_url_check=True)
    assert result == False
    assert len(problems) == 4
    assert problems[0].ErrorType == "Missing mandatory field from Package"
    assert problems[0].Reason == "There is no purl type ExternalRef field in the Package"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-nopurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[0].PackageName == "nopurl-libldap-2.4-2"
    assert problems[1].ErrorType == "Useless mandatory field from Package"
    assert problems[1].Reason == "purl (pkg:deb/not-debian/libldap-2.4-2@2.4.57+dfsg-3+deb11u1?arch=amd64&upstream=openldap&distro=debian-11) in the ExternalRef cannot be converted to a downloadable URL"
    assert problems[1].SPDX_ID == "SPDXRef-Package-deb-badpurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[1].PackageName == "badpurl-libldap-2.4-2"
    assert problems[2].ErrorType == "Invalid field in Package"
    assert problems[2].Reason == "PackageHomePage field points to a nonexisting page (https://www.not-openldap.org/)"
    assert problems[2].SPDX_ID == "SPDXRef-Package-deb-badpurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[2].PackageName == "badpurl-libldap-2.4-2"
    