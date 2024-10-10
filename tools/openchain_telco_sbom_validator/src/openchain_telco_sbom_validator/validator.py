#!/bin/python3

# © 2024 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import logging
import sys
import re
import json
from spdx_tools.spdx.model.document import Document
from spdx_tools.spdx.model.package import Package
from spdx_tools.spdx.parser import parse_anything
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.model.package import  ExternalPackageRefCategory
from spdx_tools.spdx import document_utils
from prettytable import PrettyTable
from packageurl.contrib import purl2url
import ntia_conformance_checker as ntia
import validators
import requests
import inspect

logger = logging.getLogger(__name__)
logger.propagate = True

class Problem:
    def __init__(self, ErrorType, SPDX_ID, PackageName, Reason):
        self.ErrorType = ErrorType
        self.SPDX_ID = SPDX_ID
        self.PackageName = PackageName
        self.Reason = Reason

    def __str__(self):
        return f"Problem(ErrorType={ErrorType}, SPDX_ID={SPDX_ID}, PackageName={PackageName}, Reason={Reason})"

    def __repr__(self):
        return f"Problem(ErrorType={ErrorType}, SPDX_ID={SPDX_ID}, PackageName={PackageName}, Reason={Reason})"

class Problems:
    def __init__(self):
        self.items = []

    def add(self, item: Problem):
        self.items.append(item)

    def append(self, ErrorType, SPDX_ID, PackageName, Reason):
        item = Problem(ErrorType, SPDX_ID, PackageName, Reason)
        self.add(item)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]
    def __len__(self):
        return len(self.items)

class FunctionRegistry:
    def __init__(self):
        self.functionsGlobal = []
        self.functionsPackage = []
    
    def registerPackage(self, funct):
        requiredSignature = inspect.signature(self._dummy_function_package)
        functSignature = inspect.signature(funct)
        if functSignature != requiredSignature:
            raise TypeError(f"Function {funct.__name__} does not match the required signature")
        self.functionsPackage.append(funct)

    def registerGlobal(self, funct):
        requiredSignature = inspect.signature(self._dummy_function_global)
        functSignature = inspect.signature(funct)
        if functSignature != requiredSignature:
            raise TypeError(f"Function {funct.__name__} does not match the required signature")
        self.functionsGlobal.append(funct)

    def getGlobalFunctions(self):
        return iter(self.functionsGlobal)
    
    def getPackageFunctions(self):
        return iter(self.functionsPackage)

    def _dummy_function_global(self, problems: Problems, doc: Document):
        pass

    def _dummy_function_package(self, problems: Problems, package: Package):
        pass


class Validator:

    def __init__(self):
        return None

    def validate(self, filePath, strict_purl_check=False, strict_url_check=False, functionRegistry:FunctionRegistry = FunctionRegistry()):
        """ Validates, Returns a status and a list of problems. filePath: Path to the SPDX file to validate. strict_purl_check: Not only checks the syntax of the PURL, but also checks if the package can be downloaded. strict_url_check: Checks if the given URLs in PackageHomepages can be accessed."""

        try:
            doc = parse_anything.parse_file(filePath)
        except json.decoder.JSONDecodeError as e:
            logger.error("JSON syntax error at line " + str(e.lineno) + " column " + str(e.colno))
            logger.error(e.msg)
            sys.exit(1)
        except SPDXParsingError as e:
            logger.error("ERROR! The file is not an SPDX file")
            for message in e.messages:
                logger.error(message)
            logger.error("Exiting")
            sys.exit(1)
        logger.debug("Start validating.")

        problems = Problems()

        errors = validate_full_spdx_document(doc)
        if errors:
            logger.error("ERROR! The file is not a valid SPDX file")
            for error in errors:
                logger.debug(f"Validation error: {error.context.parent_id} - {error.context.full_element} - {error.validation_message}")
                spdxId = ""
                name = ""
                if error.context.full_element is not None:
                    if hasattr(error.context.full_element, 'spdx_id'):
                        spdxId = error.context.full_element.spdx_id
                    if hasattr(error.context.full_element, 'name'):
                        name = error.context.full_element.name

                problems.append("SPDX validation error", f"{spdxId}", f"{name}", f"{error.validation_message}")

        # Checking against NTIA minimum requirements
        # No need for SPDX validation as it is done previously.
        logger.debug("Start of NTIA validation")
        sbomNTIA = ntia.SbomChecker(filePath, validate=False)
        if not sbomNTIA.ntia_minimum_elements_compliant:
            logger.debug("NTIA validation failed")
            components = sbomNTIA.get_components_without_names()
            self.ntiaErrorLog(components, problems, doc,"Package without a name")
            self.components = sbomNTIA.get_components_without_versions(return_tuples=True)
            self.ntiaErrorLogNew(components, problems, doc,"Package without a version")
            components = sbomNTIA.get_components_without_suppliers(return_tuples=True)
            self.ntiaErrorLogNew(components, problems, doc,"Package without a package supplier or package originator")
            components = sbomNTIA.get_components_without_identifiers()
            self.ntiaErrorLog(components, problems, doc,"Package without an identifyer")

        else:
            logger.debug("NTIA validation succesful")

        if doc.creation_info.creator_comment:
            logger.debug(f"CreatorComment: {doc.creation_info.creator_comment}")
            cisaSBOMTypes = ["Design", "Source", "Build", "Analyzed", "Deployed", "Runtime"]

            typeFound = False
            for cisaSBOMType in cisaSBOMTypes:
                logger.debug(f"Checking {cisaSBOMType} against {doc.creation_info.creator_comment} ({doc.creation_info.creator_comment.find(cisaSBOMType)})")
                creator_comment = doc.creation_info.creator_comment.lower();
                if -1 != doc.creation_info.creator_comment.find(cisaSBOMType):
                    logger.debug("Found")
                    typeFound = True

            if not typeFound:
                problems.append("Invalid CreationInfo", "General", "General", f"CreatorComment ({doc.creation_info.creator_comment}) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)")
        else:
            problems.append("Missing mandatory field from CreationInfo", "General", "General", f"CreatorComment is missing")

        if doc.creation_info.creators:
            organisationCorrect = False
            toolCorrect = False
            for creator in doc.creation_info.creators:
                logger.debug(f"Creator: {creator}")
                if re.match(".*Organization.*", str(creator)):
                    logger.debug(f"Creator: Organization found ({creator})")
                    organisationCorrect = True
                if re.match(".*Tool.*-.*", str(creator)):
                    logger.debug(f"Creator: Tool found with the correct format ({creator})")
                    toolCorrect = True
            if not organisationCorrect:
                problems.append("Missing or invalid field in CreationInfo::Creator", "General", "General", "There is no Creator field with Organization keyword in it")
            if not toolCorrect:
                problems.append("Missing or invalid field in CreationInfo::Creator", "General", "General","There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen")
        else:
            problems.append("Missing mandatory field from CreationInfo", "General", "General", "Creator is missing")

        for package in doc.packages:
            logger.debug(f"Package: {package}")
            if not package.version:
                problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Version field is missing")
            if not package.supplier:
                problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Supplier field is missing")
            if not package.checksums:
                problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Checksum field is missing")
            if package.external_references:
                purlFound = False
                for ref in package.external_references:
                    logger.debug(f"cat: {str(ref.category)}, type: {ref.reference_type}, locator: {ref.locator}")
                    if ref.category == ExternalPackageRefCategory.PACKAGE_MANAGER and ref.reference_type == "purl":
                        # Based on https://github.com/package-url/packageurl-python
                        purlFound = True
                        if strict_purl_check:
                            url = purl2url.get_repo_url(ref.locator)
                            if not url:
                                logger.debug("Purl (" + ref.locator + ") parsing resulted in empty result.")
                                problems.append("Useless mandatory field from Package", package.spdx_id, package.name, f"purl ({ref.locator}) in the ExternalRef cannot be converted to a downloadable URL")
                            else:
                                logger.debug(f"Strict PURL check is happy {url}")
                if not purlFound:
                    problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "There is no purl type ExternalRef field in the Package")
            else:
                problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "ExternalRef field is missing")
            if isinstance(package.homepage, type(None)):
                logger.debug("Package homepage is missing")
            else:
                logger.debug(f"Package homepage is ({package.homepage})")
                if not validators.url(package.homepage):
                    logger.debug("Package homepage is not a valid URL")
                    # Adding this to the problem list is not needed as the SPDX validator also adds it
                    # problems.append(["Invalid field in Package", package.spdx_id, package.name, f"PackageHomePage is not a valid URL ({package.homepage})"])
                else:
                    if strict_url_check:
                        try:
                            logger.debug("Checking package homepage")
                            page = requests.get(package.homepage)
                        except Exception as err:
                            logger.debug(f"Exception received ({format(err)})")
                            problems.append("Invalid field in Package", package.spdx_id, package.name, f"PackageHomePage field points to a nonexisting page ({package.homepage})")
            if functionRegistry:
                logger.debug("Calling registered package functions.")

                for function in functionRegistry.getPackageFunctions():
                    logger.debug(f"Executing function {function.__name__}({type(problems)}, {type(package)})")
                    
                    function(problems, package)

        
        if functionRegistry:
            logger.debug("Calling registered global functions.")
            for function in functionRegistry.getGlobalFunctions():
                logger.debug(f"Executing function {function.__name__}({type(problems)}, {type(doc)}")
                function(problems, doc)
        
        if problems:
            return False, problems
        else:
            return True, None

    def ntiaErrorLog(self, components, problems, doc, problemText):
        logger.debug(f"# of components: {len(components)}")
        for component in components:
            logger.debug(f"Erroneous component: {component}")
            spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
            logger.debug(f"SPDX element: {spdxPackage}")
            if spdxPackage:
                problems.append("NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText)
            else:
                problems.append("NTIA validation error", "Cannot be provided", component, problemText)

    def ntiaErrorLogNew(self, components, problems, doc, problemText):
        logger.debug(f"# of components: {len(components)}")
        for component in components:
            logger.debug(f"Erroneous component: {component}")
            if len(component) > 1:
                problems.append("NTIA validation error", component[1], component[0], problemText)
            else:
                spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
                logger.debug(f"SPDX element: {spdxPackage}")
                if spdxPackage:
                    problems.append("NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText)
                else:
                    problems.append("NTIA validation error", "Cannot be provided", component, problemText)


if __name__ == "__main__":
    main()
