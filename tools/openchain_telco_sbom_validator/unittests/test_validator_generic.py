from openchain_telco_sbom_validator import validator

import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_ok_creator_comment():
    v = validator.Validator()
    # CreatorComment: CISA SBOM Type: Analyzed
    result, problems = v.validate(filePath = "sboms/unittest-sbom-02.spdx")
    assert len(problems) == 0
    assert result == True

    # CreatorComment: SBOM Type:analyzed
    result, problems = v.validate(filePath = "sboms/unittest-sbom-13.spdx")
    assert len(problems) == 0
    assert result == True

    # CreatorComment: CISA SBOM Type: deployed
    result, problems = v.validate(filePath = "sboms/unittest-sbom-07.spdx")
    print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert len(problems) == 1
    assert result == False
    assert problems[0].ErrorType == "Missing or invalid field in CreationInfo::Creator"
    assert problems[0].Reason == "There is no Creator field with Organization keyword in it"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

    # CreatorComment: runtime
    result, problems = v.validate(filePath = "sboms/unittest-sbom-08.spdx")
    #print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert len(problems) == 0
    assert result == True

def test_nok_creator_comment_incorrect_cisa():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-09.spdx")
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "Invalid CreationInfo"
    assert problems[0].Reason == "CreatorComment (something-else) does not contain any of the CISA SBOM Types (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

def test_nok_creator_comment_missing_sbom_type():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-14.spdx", strict=True)
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "Invalid CreationInfo"
    assert problems[0].Reason == "CreatorComment (analyzed) does not follow the \"SBOM Type: type\" syntax"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

    result, problems = v.validate(filePath = "sboms/unittest-sbom-14.spdx", strict=False)
    assert result == True
    assert len(problems) == 0


def test_creator_comment_strict_non_strict():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-11.spdx", strict=True)
    print(f"{problems[1].ErrorType}, {problems[1].Reason}, {problems[1].SPDX_ID}, {problems[1].PackageName}")
    assert result == False
    assert len(problems) == 2
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a package supplier"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-Nosupplier-Nochecksum"
    assert problems[0].PackageName == "Nosupplier-Nochecksum-libldap-2.4-2"

    assert problems[1].ErrorType == "Invalid CreationInfo"
    assert problems[1].Reason == "CreatorComment (runtime) does not follow the \"SBOM Type: type\" syntax"
    assert problems[1].SPDX_ID == "General"
    assert problems[1].PackageName == "General"

    result, problems = v.validate(filePath = "sboms/unittest-sbom-11.spdx", strict=False)
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "NTIA validation error"
    assert problems[0].Reason == "Package without a package supplier"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-libldap-2.4-2-Nosupplier-Nochecksum"
    assert problems[0].PackageName == "Nosupplier-Nochecksum-libldap-2.4-2"


def test_nok_creator_comment_missing():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-10.spdx")
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "Missing mandatory field from CreationInfo"
    assert problems[0].Reason == "CreatorComment is missing"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"


