#!/bin/python3

# © 2024-2025 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import logging
import re
import os
import json
import inspect
import string
from spdx_tools.spdx.model.document import Document
from spdx_tools.spdx.model.package import Package
from spdx_tools.spdx.parser import parse_anything
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.model.package import ExternalPackageRefCategory
from spdx_tools.spdx.model.relationship import RelationshipType
from spdx_tools.spdx.model.checksum import ChecksumAlgorithm
from spdx_tools.spdx import document_utils
from packageurl.contrib import purl2url
import ntia_conformance_checker as ntia
import validators
import requests

logger = logging.getLogger(__name__)
logger.propagate = True

class Problem:
    SCOPE_FILE = "File"
    SCOPE_SPDX = "SPDX"
    SCOPE_NTIA = "NTIA"
    SCOPE_OPEN_CHAIN = "OpenChain"
    SEVERITY_ERROR = 0
    SEVERITY_NOASSERT = 1
    SEVERITY_INC_URL = 2
    SEVERITY_INC_PURL = 3
    def __init__(self, error_type, SPDX_ID, package_name, reason, scope, severity, file=""):
        self.ErrorType = error_type
        self.SPDX_ID = SPDX_ID
        self.PackageName = package_name
        self.Reason = reason
        self.file = file
        self.scope = scope
        self.severity = severity

    def __str__(self):
        if self.file:
            return f"Problem(ErrorType={self.ErrorType}, file={self.file}, SPDX_ID={self.SPDX_ID}, PackageName={self.PackageName}, Reason={self.Reason}, Scope={self.scope}, Severity={self.severity})"
        else:
            return f"Problem(ErrorType={self.ErrorType}, SPDX_ID={self.SPDX_ID}, PackageName={self.PackageName}, Reason={self.Reason}, Scope={self.scope}, Severity={self.severity})"

    def __repr__(self):
        return self.__str__()

class Problems:
    def __init__(self):
        self.items = []
        self.checked_files = []
        self.print_file = False

    def add(self, item: Problem):
        self.items.append(item)

    def append(self, error_type, SPDX_ID, package_name, reason, scope, severity, file=""):
        item = Problem(error_type, SPDX_ID, package_name, reason, scope, severity, file)
        self.add(item)

    def get_files_as_string(self):
        file_list = ""
        for file in self.checked_files[:-1]:
            file_list += f"{file}, "
        file_list += self.checked_files[-1]
        return file_list

    def do_print_file(self):
        self.print_file = True

    def get_errors(self):
        return list(problem for problem in self.items if problem.severity == Problem.SEVERITY_ERROR)

    def get_warnings(self):
        noasserts = self.get_noasserts()
        incorrect_purls = self.get_incorrect_purls()
        incorrect_urls = self.get_incorrect_urls()
        warnings = []
        if noasserts:
            warnings.extend(noasserts)
        if incorrect_purls:
            warnings.extend(incorrect_purls)
        if incorrect_urls:
            warnings.extend(incorrect_urls)
        return warnings

    def get_noasserts(self):
        return list(problem for problem in self.items if problem.severity == Problem.SEVERITY_NOASSERT)
    
    def get_incorrect_urls(self):
        return list(problem for problem in self.items if problem.severity == Problem.SEVERITY_INC_URL)

    def get_incorrect_purls(self):
        return list(problem for problem in self.items if problem.severity == Problem.SEVERITY_INC_PURL)

    def get_sorted_by_scope(self):
        return iter(sorted(self.items, key=lambda problem: problem.scope))

    def count_errors(self):
        return sum(1 for problem in self.items if problem.severity == Problem.SEVERITY_ERROR)

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __bool__(self):
        if len(self.get_errors()) > 0:
            return True
        else:
            return False

    def __str__(self):
        return f"I have {len(self.get_errors())} errors and {len(self.get_warnings())} warnings"

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
        self.referringLogicStore = {}
        self.referringLogics = {}
        self.addReferringLogics("none", referred_none)
        self.addReferringLogics("yocto-all", referred_yocto_all)
        self.addReferringLogics("yocto-contains-only", referred_yocto_contains_only)
        self.addReferringLogics("checksum-all", referred_checksum_all)

        return None

    def addReferringLogics(self, name, function):
        logger.debug(f"Registering referring logic {name}, {function}")
        requiredSignature = inspect.signature(_dummy_referred_logic)
        functSignature = inspect.signature(function)
        if functSignature != requiredSignature:
            raise TypeError(f"Function {function.__name__} does not match the required signature")
        self.referringLogics[name] = function

    def getReferringLogicNames(self):
        name_list = ""
        keys = self.referringLogics.keys()
        keys_len = len(self.referringLogics.keys())
        i = 1
        for name in keys:
            if i < keys_len:
                name_list += f"“{name}”, "
            else:
                name_list += f"“{name}”"
            i += 1
        return name_list

    def validate(self,
                 filePath,
                 strict_purl_check=False,
                 strict_url_check=False,
                 strict=False,
                 noassertion=False,
                 functionRegistry:FunctionRegistry = FunctionRegistry(),
                 problems=None,
                 referringLogic="none",
                 guide_version = "1.1"):
        """ Validates, returns a status and a list of problems.
            filePath: path to the SPDX file to validate.
            strict_purl_check: not only checks the syntax of the PURL, but also checks if the package can be downloaded.
            strict_url_check: checks if the given URLs in PackageDownloadLocation can be accessed.
            strict: checks for both MANDATORY and RECOMMENDED fields.
            noassertion: lists fields with value NOASSERTION.
            functionRegistry: is an optionsl functionRegistry class to inject custom checks.
            problems: is the problem list for linked SBOM handling.
            referringLogic: defines the logic how to determine the location of referred files."""

        logger.debug("----------------- Validate called ----------------------")
        current_frame = inspect.currentframe()
        caller_frame = inspect.getouterframes(current_frame, 2)
        if caller_frame and caller_frame[1].function == self.validate.__name__:
            logger.debug("Validate was called recursively")
            problems.do_print_file()

        if problems == None:
            problems = Problems()
        else:
            logger.debug(f"Inherited {len(problems)} problems")

        file_path_full = os.path.basename(filePath)

        if file_path_full in problems.checked_files:
            logger.debug(f"File ({file_path_full}) already checked")
            if problems:
                return False, problems
            else:
                return True, problems

        problems.checked_files.append(file_path_full)

        if filePath == "":
            logger.error(f"File path is a mandatory parameter.")
            problems.append("File error",
                            "General",
                            "General",
                            f"File path is empty",
                            Problem.SCOPE_FILE,
                            Problem.SEVERITY_ERROR,
                            filePath)
            return False, problems

        if not os.path.isfile(filePath):
            logger.error(f"File does not exist {filePath}")
            problems.append("File error",
                            "General",
                            "General",
                            f"File does not exist ({filePath})",
                            Problem.SCOPE_FILE,
                            Problem.SEVERITY_ERROR,
                            filePath)
            return False, problems

        file = os.path.basename(filePath)
        dir_name = os.path.dirname(filePath)
        match = re.search(r'\.(.+)$', file)
        extension = ""
        if match:
            extension = match.group(1)
        logger.debug(f"File path is {dir_name}, filename is {file}, extension is {extension}")
        print(f"Validating {file}")


        try:
            doc = parse_anything.parse_file(filePath)
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSON syntax error at line {e.lineno} column {e.colno}")
            logger.error(e.msg)
            problems.append("File error",
                            "General",
                            "General",
                            f"JSON syntax error at line {e.lineno} column {e.colno}",
                            Problem.SCOPE_FILE,
                            Problem.SEVERITY_ERROR,
                            file)
            return False, problems
        except SPDXParsingError as e:
            logger.error(f"ERROR! The file ({filePath}) is not an SPDX file")
            all_messages = ""
            for message in e.messages:
                logger.error(message)
            problems.append("File error",
                            "",
                            "",
                            "The file is not an SPDX file",
                            Problem.SCOPE_FILE,
                            Problem.SEVERITY_ERROR,
                            file)
            return False, problems

        logger.debug("Start validating.")

        errors = validate_full_spdx_document(doc)
        if errors:
            logger.error(f"The file ({filePath}) is not a valid SPDX file")
            for error in errors:
                logger.debug(f"Validation error: {error.context.parent_id} - {error.context.full_element} - {error.validation_message}")
                spdxId = "General"
                name = "General"
                if error.context.full_element is not None:
                    if hasattr(error.context.full_element, 'spdx_id'):
                        spdxId = error.context.full_element.spdx_id
                    if hasattr(error.context.full_element, 'name'):
                        name = error.context.full_element.name

                problems.append("SPDX validation error",
                                f"{spdxId}",
                                f"{name}",
                                f"{error.validation_message}",
                                Problem.SCOPE_SPDX,
                                Problem.SEVERITY_ERROR,
                                file)

        # Checking against NTIA minimum requirements
        # No need for SPDX validation as it is done previously.
        logger.debug("Start of NTIA validation")
        sbomNTIA = ntia.SbomChecker(filePath, validate=False)
        if not sbomNTIA.ntia_minimum_elements_compliant:
            logger.debug("NTIA validation failed")
            components = sbomNTIA.get_components_without_names()
            #logger.debug(f"components: {components}, problems: {str(problems)}, doc: {doc}")
            self.__ntiaErrorLog(components, problems, doc, "Package without a name", file)
            components = sbomNTIA.get_components_without_versions(return_tuples=True)
            self.__ntiaErrorLogNew(components, problems, doc, "Package without a version", file)
            components = sbomNTIA.get_components_without_suppliers(return_tuples=True)
            self.__ntiaErrorLogNew(components, problems, doc, "Package without a package supplier", file)
            components = sbomNTIA.get_components_without_identifiers()
            self.__ntiaErrorLog(components, problems, doc, "Package without an identifier", file)

        else:
            logger.debug("NTIA validation succesful")

        if doc.creation_info.creator_comment:
            logger.debug(f"CreatorComment: {doc.creation_info.creator_comment}")
            cisaSBOMTypes = ["design", "source", "build", "analyzed", "deployed", "runtime"]
            creator_comment = doc.creation_info.creator_comment.lower().strip()
            if strict:
                logger.debug(f"Strict check is on")
                match = re.search(r'sbom type:\s*(\w+)', creator_comment)
                sbom_type = None

                if match:
                    sbom_type = match.group(1)

                    if not sbom_type in cisaSBOMTypes:
                        logger.debug(f"SBOM Type in CreatorComment ({sbom_type}) is not in the CISA SBOM Type list ({cisaSBOMTypes})")
                        problems.append("Invalid CreationInfo",
                                        "General",
                                        "General",
                                        f"CreatorComment ({doc.creation_info.creator_comment}) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)",
                                        Problem.SCOPE_OPEN_CHAIN,
                                        Problem.SEVERITY_ERROR,
                                        file)
                    else:
                        logger.debug(f"CreatorComment ({doc.creation_info.creator_comment}) is in the CISA SBOM Type list ({cisaSBOMTypes})")
                else:
                    logger.debug(f"CreatorComment ({doc.creation_info.creator_comment}) does not follow the \"SBOM Type: type\" syntax")
                    problems.append("Invalid CreationInfo",
                                    "General",
                                    "General",
                                    f"CreatorComment ({doc.creation_info.creator_comment}) does not follow the \"SBOM Type: type\" syntax",
                                    Problem.SCOPE_OPEN_CHAIN,
                                    Problem.SEVERITY_ERROR,
                                    file)

            else:
                # Handle "SBOM Type:analyzed"
                creator_comment = creator_comment.replace(':', ' ')
                # Remove punctuation
                translator = str.maketrans('', '', string.punctuation)
                creator_comment = creator_comment.translate(translator)
                tokens = re.split(r'[ :]+', creator_comment)
                logger.debug(f"Strict check is off. (CreatorComment words: {tokens})")
                if not any(sbom_type in tokens for sbom_type in cisaSBOMTypes):
                    logger.debug(f"CreatorComment ({doc.creation_info.creator_comment}) does not contain any of the CISA SBOM Types ({cisaSBOMTypes})")
                    problems.append("Invalid CreationInfo",
                                    "General",
                                    "General",
                                    f"CreatorComment ({doc.creation_info.creator_comment}) does not contain any of the CISA SBOM Types (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)",
                                    Problem.SCOPE_OPEN_CHAIN,
                                    Problem.SEVERITY_ERROR,
                                    file)
                else:
                    logger.debug(f"CreatorComment ({doc.creation_info.creator_comment}) contains one of the items from the CISA SBOM Type list ({cisaSBOMTypes})")
        else:
            problems.append("Missing mandatory field from CreationInfo",
                            "General",
                            "General",
                            f"CreatorComment is missing",
                            Problem.SCOPE_OPEN_CHAIN,
                            Problem.SEVERITY_ERROR,
                            file)

        if doc.creation_info.creators:
            organisationCorrect = False
            toolCorrect = False
            for creator in doc.creation_info.creators:
                logger.debug(f"Creator: {creator}")
                if re.match(".*Organization.*", str(creator)):
                    logger.debug(f"Creator: Organization found ({creator})")
                    organisationCorrect = True
                # In strict mode (RECOMMENDED), we check there is an hyphen between tool name and version
                # and there is a single hyphen
                if strict:
                    if re.match(".*Tool.*-.*", str(creator)) and str(creator).count('-') == 1:
                        logger.debug(f"Creator: Tool and version found with the correct format ({creator})")
                        toolCorrect = True
                else:
                    if re.match(".*Tool.*", str(creator)):
                        logger.debug(f"Creator: Tool found with the correct format ({creator})")
                        toolCorrect = True
            if not organisationCorrect:
                problems.append("Missing or invalid field in CreationInfo::Creator",
                                "General",
                                "General",
                                "There is no Creator field with Organization keyword in it",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_ERROR, file)
            if not toolCorrect:
                if strict:
                    problems.append("Missing or invalid field in CreationInfo::Creator",
                                    "General",
                                    "General",
                                    "There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen",
                                    Problem.SCOPE_OPEN_CHAIN,
                                    Problem.SEVERITY_ERROR,
                                    file)
                else:
                    problems.append("Missing or invalid field in CreationInfo::Creator",
                                    "General",
                                    "General",
                                    "There is no Creator field with Tool keyword in it",
                                    Problem.SCOPE_OPEN_CHAIN,
                                    Problem.SEVERITY_ERROR,
                                    file)
        else:
            problems.append("Missing mandatory field from CreationInfo",
                            "General",
                            "General",
                            "Creator is missing",
                            Problem.SCOPE_OPEN_CHAIN,
                            Problem.SEVERITY_ERROR,
                            file)

        for package in doc.packages:
            logger.debug(f"Package: {package}")

            # License concluded is mandatory in SPDX 2.2, but not in SPDX 2.3
            # It is mandatory in OpenChain Telco SBOM Guide
            if not hasattr(package, 'license_concluded'):
                problems.append("Missing mandatory field from Package",
                                package.spdx_id,
                                package.name,
                                "License concluded field is missing",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_ERROR,
                                file)
            elif noassertion and (str(package.license_concluded) == "NOASSERTION"):
                problems.append("Field with NOASSERTION",
                                package.spdx_id,
                                package.name,
                                "License concluded is NOASSERTION",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_NOASSERT, file)

            # License declared is mandatory in SPDX 2.2, but not in SPDX 2.3
            # It is mandatory in OpenChain Telco SBOM Guide
            if not hasattr(package, 'license_declared'):
                problems.append("Missing mandatory field from Package",
                                package.spdx_id,
                                package.name,
                                "License declared field is missing",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_ERROR,
                                file)
            elif noassertion and (str(package.license_declared) == "NOASSERTION"):
                problems.append("Field with NOASSERTION",
                                package.spdx_id,
                                package.name,
                                "License declared is NOASSERTION",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_NOASSERT,
                                file)

            # Package copyright text is mandatory in SPDX 2.2, but not in SPDX 2.3
            # It is mandatory in OpenChain Telco SBOM Guide
            if not hasattr(package, 'copyright_text'):
                problems.append("Missing mandatory field from Package",
                                package.spdx_id,
                                package.name,
                                "Copyright text field is missing",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_ERROR,
                                file)
            elif noassertion and (str(package.copyright_text) == "NOASSERTION"):
                problems.append("Field with NOASSERTION",
                                package.spdx_id,
                                package.name,
                                "Copyright text is NOASSERTION",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_NOASSERT,
                                file)

            if noassertion and (str(package.download_location) == "NOASSERTION"):
                problems.append("Field with NOASSERTION",
                                package.spdx_id,
                                package.name,
                                "Download location is NOASSERTION",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_NOASSERT,
                                file)

            if hasattr(package, 'external_references'):
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
                                problems.append("Useless mandatory field from Package",
                                                package.spdx_id,
                                                package.name,
                                                f"purl ({ref.locator}) in the ExternalRef cannot be converted to a downloadable URL",
                                                Problem.SCOPE_OPEN_CHAIN,
                                                Problem.SEVERITY_INC_PURL,
                                                file)
                            else:
                                logger.debug(f"Strict PURL check is happy {url}")
                if strict and not purlFound:
                    problems.append("Missing mandatory field from Package",
                                    package.spdx_id,
                                    package.name,
                                    "There is no purl type ExternalRef field in the Package",
                                    Problem.SCOPE_OPEN_CHAIN,
                                    Problem.SEVERITY_ERROR,
                                    file)
            elif strict:
                problems.append("Missing mandatory field from Package",
                                package.spdx_id,
                                package.name,
                                "ExternalRef field is missing (no Package URL)",
                                Problem.SCOPE_OPEN_CHAIN,
                                Problem.SEVERITY_ERROR, file)
            if isinstance(package.download_location, type(None)):
                logger.debug("PackageDownloadLocation is missing")
            else:
                logger.debug(f"PackageDownloadLocation is ({package.download_location})")
                if not validators.url(package.download_location):
                    logger.debug("PackageDownloadLocation not a valid URL")
                    # Adding this to the problem list is not needed as the SPDX validator also adds it
                    # problems.append(["Invalid field in Package", package.spdx_id, package.name, f"PackageDownloadLocation a valid URL ({package.download_location})"])
                else:
                    if strict_url_check:
                        try:
                            logger.debug("Checking PackageDownloadLocation")
                            page = requests.get(package.download_location)
                        except Exception as err:
                            logger.debug(f"Exception received ({format(err)})")
                            problems.append("Invalid field in Package",
                                            package.spdx_id,
                                            package.name,
                                            f"PackageDownloadLocation field points to a nonexisting page ({package.download_location})",
                                            Problem.SCOPE_OPEN_CHAIN,
                                            Problem.SEVERITY_INC_URL,
                                            file)
            # Version specifics
            match guide_version:
                case "1.0":
                    if not package.checksums:
                        problems.append("Missing mandatory field from Package",
                                        package.spdx_id,
                                        package.name,
                                        "PackageChecksum field is missing",
                                        Problem.SCOPE_OPEN_CHAIN,
                                        Problem.SEVERITY_ERROR,
                                        file)
                    if not package.files_analyzed:
                        problems.append("Missing mandatory field from Package",
                                        package.spdx_id,
                                        package.name,
                                        "FilesAnalyzed field is missing",
                                        Problem.SCOPE_OPEN_CHAIN,
                                        Problem.SEVERITY_ERROR,
                                        file)
                case "1.1":
                    if strict and (not (package.checksums or package.verification_code)):
                        problems.append("Missing mandatory field from Package",
                                        package.spdx_id,
                                        package.name,
                                        "Both PackageChecksum and PackageVerificationCode fields are missing",
                                        Problem.SCOPE_OPEN_CHAIN,
                                        Problem.SEVERITY_ERROR,
                                        file)
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

        list_of_referred_sboms = []

        if referringLogic in self.referringLogics:
            logger.debug(f"Executing referring logic: {referringLogic},  {self.referringLogics[referringLogic]}")
            list_of_referred_sboms, problems = self.referringLogics[referringLogic](self, doc, dir_name, problems, extension)
        else:
            logger.error(f"Referring logic “{referringLogic}” is not in the registered referring logic list {self.getReferringLogicNames()}")
            print(f"Referring logic error. Referring logic “{referringLogic}” is not in the registered referring logic list {self.getReferringLogicNames()}")
            return False, problems

        for referred_sbom in list_of_referred_sboms:
            self.validate(
                filePath=referred_sbom,
                strict_purl_check=strict_purl_check,
                strict_url_check=strict_url_check,
                functionRegistry=functionRegistry,
                problems=problems,
                referringLogic=referringLogic,
                noassertion=noassertion)
        if problems:
            return False, problems
        else:
            return True, problems

    def __ntiaErrorLog(self, components, problems, doc, problemText, file):
        logger.debug(f"# of components: {len(components)}")
        for component in components:
            logger.debug(f"Erroneous component: {component}")
            spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
            logger.debug(f"SPDX element: {spdxPackage}")
            if spdxPackage:
                problems.append("NTIA validation error",
                                spdxPackage.spdx_id,
                                spdxPackage.name,
                                problemText,
                                Problem.SCOPE_NTIA,
                                Problem.SEVERITY_ERROR,
                                file)
            else:
                problems.append("NTIA validation error",
                                "Cannot be provided",
                                component,
                                problemText,
                                Problem.SCOPE_NTIA,
                                Problem.SEVERITY_ERROR,
                                file)

    def __ntiaErrorLogNew(self, components, problems, doc, problemText, file):
        logger.debug(f"# of components: {len(components)}")
        for component in components:
            logger.debug(f"Erroneous component: {component}")
            if len(component) > 1:
                problems.append("NTIA validation error",
                                component[1],
                                component[0],
                                problemText,
                                Problem.SCOPE_NTIA,
                                Problem.SEVERITY_ERROR,
                                file)
            else:
                spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
                logger.debug(f"SPDX element: {spdxPackage}")
                if spdxPackage:
                    problems.append("NTIA validation error",
                                    spdxPackage.spdx_id,
                                    spdxPackage.name,
                                    problemText,
                                    Problem.SCOPE_NTIA,
                                    Problem.SEVERITY_ERROR,
                                    file)
                else:
                    problems.append("NTIA validation error",
                                    "Cannot be provided",
                                    component,
                                    problemText,
                                    Problem.SCOPE_NTIA,
                                    Problem.SEVERITY_ERROR,
                                    file)

def referred_yocto_all(self, doc: Document, dir_name: str, problems: Problems, extension: str=""):
    logger.debug(f"In Yocto all. Extension is {extension}")
    documents = []
    ref_base = ""
    if doc.creation_info.document_namespace:
        # http://spdx.org/spdxdoc/recipe-serviceuser-user-7abdc33d-d61f-549c-a5f7-05ffbd5118e8
        result = re.search("^(.*/)[\w-]+$", doc.creation_info.document_namespace)
        if result:
            ref_base = result.group(1)
            logger.debug(f"Reference base is {ref_base}")

    if doc.creation_info.external_document_refs:
        logger.debug(f"There are references")
        for ref in doc.creation_info.external_document_refs:
            logger.debug(f"SPDX document referenced {ref.document_uri}")
            doc_location = str(ref.document_uri).replace(ref_base, "")
            #logger.debug(f"Doc location 1: {doc_location}")
            # Assumption is that the UUID looks like this: c146050a-959a-5836-966f-98e79d6e765f
            # 8-4-4-4-12
            result = re.search("([\w\.-]+)-[\w-]{8}(-[\w-]{4}){3}-[\w-]{12}$", doc_location)
            if result:
                doc_location = result.group(1)
                if dir_name == "":
                    doc_location = f"{doc_location}.{extension}"
                else:
                    doc_location = f"{dir_name}/{doc_location}.{extension}"
                logger.debug(f"Document location is: {doc_location}")
                documents.append(doc_location)
    return documents, problems

def referred_yocto_contains_only(self, doc: Document, dir_name: str, problems: Problems, extension: str=""):
    logger.debug("In Yocto contains only")
    documents = []
    ref_base = ""
    if doc.creation_info.document_namespace:
        # http://spdx.org/spdxdoc/recipe-serviceuser-user-7abdc33d-d61f-549c-a5f7-05ffbd5118e8
        result = re.search("^(.*/)[\w-]+$", doc.creation_info.document_namespace)
        if result:
            ref_base = result.group(1)
            logger.debug(f"Reference base is {ref_base}")
    external_refs = {}
    if doc.creation_info.external_document_refs:
        logger.debug(f"--------------We have refs!------------")
        for ref in doc.creation_info.external_document_refs:
            logger.debug(f"SPDX document referenced {ref.document_uri}")
            doc_location = str(ref.document_uri).replace(ref_base, "")
            #logger.debug(f"Doc location 1: {doc_location}")
            # Assumption is that the UUID looks like this: c146050a-959a-5836-966f-98e79d6e765f
            # 8-4-4-4-12
            result = re.search("([\w\.-]+)-[\w-]{8}(-[\w-]{4}){3}-[\w-]{12}$", doc_location)
            if result:
                doc_location = result.group(1)
                if dir_name == "":
                    doc_location = f"{doc_location}.spdx.json"
                else:
                    doc_location = f"{dir_name}/{doc_location}.spdx.json"
                logger.debug(f"Document location is: {doc_location}, ref: {ref.document_ref_id}")
                external_refs[ref.document_ref_id] = doc_location
    if doc.relationships:
        for relationship in doc.relationships:
            if relationship.relationship_type == RelationshipType.CONTAINS:
                spdx_document_id = relationship.related_spdx_element_id.split(":")[0]
                logger.debug(f"SPDX document is {spdx_document_id}")
                if spdx_document_id in external_refs:
                    logger.debug(f"Adding {external_refs[spdx_document_id]} to the referred file list")
                    documents.append(external_refs[spdx_document_id])
    return documents, problems

def referred_checksum_all(self, doc: Document, dir_name: str, problems: Problems, extension: str=""):
    # Known limitations: MD2, MD4 and MD6 hashes are not supported
    import hashlib
    from pathlib import Path
    logger.debug("In Referred checksum all")
    documents = []
    checksums = {}
    algorithms = {}
    if doc.creation_info.external_document_refs:
        logger.debug(f"--------------We have refs!------------")
        for ref in doc.creation_info.external_document_refs:
            logger.debug(f"SPDX document referenced {ref.document_ref_id}, {ref.document_uri}, {ref.checksum.algorithm}, {ref.checksum.value}")
            if ref.checksum.algorithm in self.referringLogicStore.keys():
                if ref.checksum.value in self.referringLogicStore[ref.checksum.algorithm].keys():
                    logger.debug(f"Document found in LogicStore {ref.checksum.algorithm}, {ref.checksum.value}")
                    documents.append(self.referringLogicStore[ref.checksum.algorithm][ref.checksum.value])
            if not ref.checksum.algorithm in checksums.keys():
                logger.debug(f"{ref.document_ref_id}: {ref.checksum.algorithm} is not in checksum keys")
                checksums[ref.checksum.algorithm] = {}
                checksums[ref.checksum.algorithm][ref.checksum.value] = ref.document_ref_id
            else:
                logger.debug(f"{ref.document_ref_id}: {ref.checksum.algorithm} is in checksum keys")
                if not ref.checksum.value in checksums[ref.checksum.algorithm].keys():
                    logger.debug(f"{ref.document_ref_id}: {ref.checksum.value} is not in checksum list")
                    checksums[ref.checksum.algorithm][ref.checksum.value] = ref.document_ref_id
            algorithms[ref.checksum.algorithm] = None
            logger.debug(f"checksums: {checksums}")
            logger.debug(f"algorithms: {algorithms}")
            logger.debug(f"logicStore: {self.referringLogicStore}")
    for algorithm in algorithms.keys():
        for spdx_file in [f.name for f in Path(dir_name).iterdir() if f.is_file()]:
            logger.debug(f"Calculating {algorithm} hash for {dir_name}, {spdx_file}")
            if dir_name == "":
                doc_location = spdx_file
            else:
                doc_location = f"{dir_name}/{spdx_file}"
            logger.debug(f"Document location is: {doc_location}")
            with open(doc_location, 'rb') as f:
                hash = None
                # SHA1, SHA224, SHA256, SHA384, SHA512, MD2, MD4, MD5, MD6
                match algorithm:
                    case ChecksumAlgorithm.SHA1:
                        hash = hashlib.sha1()
                    case ChecksumAlgorithm.SHA224:
                        hash = hashlib.sha224()
                    case ChecksumAlgorithm.SHA256:
                        hash = hashlib.sha256()
                    case ChecksumAlgorithm.SHA384:
                        hash = hashlib.sha384()
                    case ChecksumAlgorithm.SHA512:
                        hash = hashlib.sha512()
                    case ChecksumAlgorithm.MD5:
                        hash = hashlib.md5()
                    case _:
                        logger.error(f"{algorithm} is not supported.")

                while chunk := f.read(8192):
                    hash.update(chunk)
            logger.debug(f"Storing file information for {algorithm}, {doc_location}, {hash.name},  {hash.hexdigest()}")
            if algorithm not in self.referringLogicStore:
                self.referringLogicStore[algorithm] = {}
            self.referringLogicStore[algorithm][hash.hexdigest()] = doc_location
    for algorithm in checksums.keys():
        for checksum in checksums[algorithm].keys():
            logger.debug(f"Getting information from Logic Store for {algorithm}, {checksum}")
            if algorithm in self.referringLogicStore:
                if checksum in self.referringLogicStore[algorithm]:
                    documents.append(self.referringLogicStore[algorithm][checksum])
                else:
                    logger.error(f"Checksum not found in Logic Store {algorithm}, {checksum}, Document Ref: {checksums[algorithm][checksum]}")
                    problems.append("File error",
                                    "General",
                                    "General",
                                    f"Non existing file referenced (Checksum: {algorithm}, {checksum}, Document Ref: {checksums[algorithm][checksum]})",
                                    Problem.SCOPE_FILE,
                                    Problem.SEVERITY_ERROR,
                                    "")
            else:
                logger.error(f"Algorithm not found in Logic Store {algorithm}, {checksum}")

    documents_dd = set()
    documents_dd = [x for x in documents if not (x in documents_dd or documents_dd.add(x))]

    logger.debug(f"documents_dd: {documents_dd}")

    return documents_dd, problems

def referred_none(self, doc: Document, dir_name: str, problems: Problems, extension: str=""):
    return [], problems

def _dummy_referred_logic(self, doc: Document, dir_name: str, problems: Problems, extension: str = ""):
    pass
