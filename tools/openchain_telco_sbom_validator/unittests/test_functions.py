from spdx_tools.spdx.model.package import Package
from spdx_tools.spdx.model.document import Document
from openchain_telco_sbom_validator import validator

def test_nok_package_function():
    v = validator.Validator()
    functions = validator.FunctionRegistry()
    functions.registerPackage(checkPackageHomepage)
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", functionRegistry=functions)
    assert result == False
    assert len(problems) == 3
    assert problems[0].ErrorType == "Invalid CreationInfo"
    assert problems[0].Reason == "CreatorComment (runtime) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

    assert problems[1].ErrorType == "Missing mandatory field from Package"
    assert problems[1].Reason == "There is no purl type ExternalRef field in the Package"
    assert problems[1].SPDX_ID == "SPDXRef-Package-deb-nopurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[1].PackageName == "nopurl-libldap-2.4-2"

    assert problems[2].ErrorType == "Missing mandatory field from Package"
    assert problems[2].Reason == "PackageHomePage field is missing"
    assert problems[2].SPDX_ID == "SPDXRef-Package-deb-nohomepage-libldap-2.4-2-796a192b709a2a2b"
    assert problems[2].PackageName == "nohomepage-libldap-2.4-2"


def checkPackageHomepage(problems: validator.Problems, package: Package):
    if isinstance(package.homepage, type(None)):
        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "PackageHomePage field is missing")


def test_nok_global_function():
    v = validator.Validator()
    functions = validator.FunctionRegistry()
    functions.registerGlobal(checkSPDXVersion)
    result, problems = v.validate(filePath = "sboms/unittest-sbom-12.spdx", functionRegistry=functions)
    assert result == False
    assert len(problems) == 3

    assert problems[0].ErrorType == "Invalid CreationInfo"
    assert problems[0].Reason == "CreatorComment (runtime) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)"
    assert problems[0].SPDX_ID == "General"
    assert problems[0].PackageName == "General"

    assert problems[1].ErrorType == "Missing mandatory field from Package"
    assert problems[1].Reason == "There is no purl type ExternalRef field in the Package"
    assert problems[1].SPDX_ID == "SPDXRef-Package-deb-nopurl-libldap-2.4-2-796a192b709a2a2b"
    assert problems[1].PackageName == "nopurl-libldap-2.4-2"

    assert problems[2].ErrorType == "SPDX Version"
    assert problems[2].Reason == "SPDX Version is SPDX-2.3"
    assert problems[2].SPDX_ID == "General"
    assert problems[2].PackageName == "General"

def checkSPDXVersion(problems: validator.Problems, doc: Document):
    if doc.creation_info.spdx_version == "SPDX-2.3":
        problems.append("SPDX Version", "General", "General", f"SPDX Version is SPDX-2.3")
