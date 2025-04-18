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
    # CreatorComment: CISA SBOM Type: analyzed
    result, problems = v.validate(filePath = "sboms/unittest-sbom-07.spdx")
    assert len(problems) == 2
    assert result == False
    assert problems[0].ErrorType == "Missing or invalid field in CreationInfo::Creator"
    assert problems[0].Reason == "There is no Creator field with Organization keyword in it"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"
    assert problems[1].ErrorType == "Missing or invalid field in CreationInfo::Creator"
    assert problems[1].Reason == "There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen"
    assert problems[1].SPDX_ID == "General"
    assert problems[1].PackageName == "General"

    # CreatorComment: runtime
    result, problems = v.validate(filePath = "sboms/unittest-sbom-08.spdx")
    assert len(problems) == 0
    assert result == True

def test_nok_creater_comment_incorrect_cisa():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-09.spdx")
    assert result == False
    assert len(problems) == 1
    assert problems[0].ErrorType == "Invalid CreationInfo"
    assert problems[0].Reason == "CreatorComment (something-else) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

def test_nok_creater_comment_missing():
    v = validator.Validator()
    result, problems = v.validate(filePath = "sboms/unittest-sbom-10.spdx")
    assert result == False
    assert len(problems) == 2
    assert problems[0].ErrorType == "Missing mandatory field from CreationInfo"
    assert problems[0].Reason == "CreatorComment is missing"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"
    assert problems[1].ErrorType == "Missing or invalid field in CreationInfo::Creator"
    assert problems[1].Reason == "There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen"
    assert problems[1].SPDX_ID == "General"
    assert problems[1].PackageName == "General"


