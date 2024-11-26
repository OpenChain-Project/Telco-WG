from openchain_telco_sbom_validator import validator
import logging

logger = logging.getLogger(__name__)
logger.propagate = True

logLevel = logging.DEBUG
logger.debug("Debug logging is ON")



def test_nok_empty_file():
    v = validator.Validator()
    result, problems = v.validate("")
    assert problems[0].ErrorType == "File error"
    assert result == False

def test_nok_not_spdx():
    v = validator.Validator()
    result, problems = v.validate( "test_validator_basic_errors.py")
    assert problems[0].ErrorType == "File error"
    assert result == False

def test_nok_json_error():
    v = validator.Validator()
    result, problems = v.validate("sboms/unittest-sbom-03.spdx.json")
    assert problems[0].ErrorType == "File error"
    assert result == False

def test_nok_not_valid_spdx():
    v = validator.Validator()
    result, problems = v.validate("sboms/unittest-sbom-04.spdx")
    assert problems[0].ErrorType == "SPDX validation error"
    assert result == False
