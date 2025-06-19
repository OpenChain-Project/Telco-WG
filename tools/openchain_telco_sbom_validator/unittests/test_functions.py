from spdx_tools.spdx.model.package import Package
from spdx_tools.spdx.model.document import Document
from openchain_telco_sbom_validator import validator
from openchain_telco_sbom_validator.validator import Problem
def test_nok_package_function():
    v = validator.Validator()
    functions = validator.FunctionRegistry()
    functions.registerPackage(checkPackageHomepage)
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", functionRegistry=functions)
    print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert result == False
    assert len(problems) == 1

    assert problems[0].ErrorType == "Missing mandatory field from Package"
    assert problems[0].Reason == "PackageHomePage field is missing"
    assert problems[0].SPDX_ID == "SPDXRef-Package-deb-nohomepage-libldap-2.4-2-796a192b709a2a2b"
    assert problems[0].PackageName == "nohomepage-libldap-2.4-2"

def checkPackageHomepage(problems: validator.Problems, package: Package):
    if isinstance(package.homepage, type(None)):
        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "PackageHomePage field is missing",Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR)


def test_nok_global_function():
    v = validator.Validator()
    functions = validator.FunctionRegistry()
    functions.registerGlobal(checkSPDXVersion)
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", functionRegistry=functions)
    print(f"{problems[0].ErrorType}, {problems[0].Reason}, {problems[0].SPDX_ID}, {problems[0].PackageName}")
    assert result == False
    assert len(problems) == 1

    assert problems[0].ErrorType == "SPDX Version"
    assert problems[0].Reason == "SPDX Version is SPDX-2.3"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

def checkSPDXVersion(problems: validator.Problems, doc: Document):
    if doc.creation_info.spdx_version == "SPDX-2.3":
        problems.append("SPDX Version", "General", "General", f"SPDX Version is SPDX-2.3", Problem.SCOPE_OPEN_CHAIN, Problem.SEVERITY_ERROR)
