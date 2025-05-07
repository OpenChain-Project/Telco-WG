#!/bin/python3

# © 2024-2025 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import logging
import re
import os
import sys
import json
from spdx_tools.spdx.model.document import Document
from spdx_tools.spdx.model.package import Package
from spdx_tools.spdx.parser import parse_anything
from spdx_tools.spdx.validation.document_validator import validate_full_spdx_document
from spdx_tools.spdx.parser.error import SPDXParsingError
from spdx_tools.spdx.model.package import  ExternalPackageRefCategory
from spdx_tools.spdx.model.relationship import RelationshipType
from spdx_tools.spdx.model.checksum import ChecksumAlgorithm
from spdx_tools.spdx import document_utils
from packageurl.contrib import purl2url
import ntia_conformance_checker as ntia
import validators
import requests
import inspect

logger = logging.getLogger(__name__)
logger.propagate = True

class Problem:
    def __init__(self, ErrorType, SPDX_ID, PackageName, Reason, file=""):
        self.ErrorType = ErrorType
        self.SPDX_ID = SPDX_ID
        self.PackageName = PackageName
        self.Reason = Reason
        self.file = file

    def __str__(self):
        if self.file:
            return f"Problem(ErrorType={self.ErrorType}, file={self.file}, SPDX_ID={self.SPDX_ID}, PackageName={self.PackageName}, Reason={self.Reason})"
        else:
            return f"Problem(ErrorType={self.ErrorType}, SPDX_ID={self.SPDX_ID}, PackageName={self.PackageName}, Reason={self.Reason})"

    def __repr__(self):
        return self.__str__(self)

class Problems:
    def __init__(self):
        self.items = []
        self.checked_files = []
        self.print_file = False

    def add(self, item: Problem):
        self.items.append(item)

    def append(self, ErrorType, SPDX_ID, PackageName, Reason, file=""):
        item = Problem(ErrorType, SPDX_ID, PackageName, Reason, file)
        self.add(item)

    def get_files_as_string(self):
        file_list = ""
        for file in self.checked_files[:-1]:
            file_list += f"{file}, "
        file_list += self.checked_files[-1]
        return file_list

    def do_print_file(self):
        self.print_file = True

    def __iter__(self):
        return iter(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __len__(self):
        return len(self.items)

    def __bool__(self):
        if len(self.items) > 0:
            return True
        else:
            return False
    def __str__(self):
        return f"I have {len(self.items)} problems"

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
                 functionRegistry:FunctionRegistry = FunctionRegistry(),
                 problems=None,
                 referringLogic="none",
                 guide_version = "1.1"):
        """ Validates, Returns a status and a list of problems.
            filePath: Path to the SPDX file to validate.
            strict_purl_check: Not only checks the syntax of the PURL, but also checks if the package can be downloaded.
            strict_url_check: Checks if the given URLs in PackageHomepages can be accessed.
            functionRegistry: is an optionsl functionRegistry class to inject custom checks.
            problems: is the problem list for linked SBOM handling
            referringLogic: defines the logic how to determine the location of referred files"""

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
            problems.append("File error", "General", "General", f"File path is empty", filePath)
            return False, problems

        if not os.path.isfile(filePath):
            logger.error(f"File does not exist {filePath}")
            problems.append("File error", "General", "General", f"File does not exist ({filePath})", filePath)
            return False, problems

        file = os.path.basename(filePath)
        dir_name = os.path.dirname(filePath)
        logger.debug(f"File path is {dir_name}, filename is {file}")
        print(f"Validating {file}")


        try:
            doc = parse_anything.parse_file(filePath)
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSON syntax error at line {e.lineno} column {e.colno}")
            logger.error(e.msg)
            problems.append("File error", "General", "General", f"JSON syntax error at line {e.lineno} column {e.colno}", file)
            return False, problems
        except SPDXParsingError as e:
            logger.error(f"ERROR! The file ({filePath}) is not an SPDX file")
            all_messages = ""
            for message in e.messages:
                logger.error(message)
            problems.append("File error", "", "", "The file is not an SPDX file", file)
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

                problems.append("SPDX validation error", f"{spdxId}", f"{name}", f"{error.validation_message}", file)

        # Checking against NTIA minimum requirements
        # No need for SPDX validation as it is done previously.
        logger.debug("Start of NTIA validation")
        sbomNTIA = ntia.SbomChecker(filePath, validate=False)
        if not sbomNTIA.ntia_minimum_elements_compliant:
            logger.debug("NTIA validation failed")
            components = sbomNTIA.get_components_without_names()
            #logger.debug(f"components: {components}, problems: {str(problems)}, doc: {doc}")
            self.__ntiaErrorLog(components, problems, doc, "Package without a name", file)

            #self.ntiaErrorLog(components, problems, doc, "Package without a name")
            #self.ntiaErrorLogNew(components, problems, doc, "Package without a version")
            components = sbomNTIA.get_components_without_versions(return_tuples=True)
            self.__ntiaErrorLogNew(components, problems, doc, "Package without a version", file)
            components = sbomNTIA.get_components_without_suppliers(return_tuples=True)
            self.__ntiaErrorLogNew(components, problems, doc, "Package without a package supplier", file)
            components = sbomNTIA.get_components_without_identifiers()
            self.__ntiaErrorLog(components, problems, doc, "Package without an identifyer", file)

        else:
            logger.debug("NTIA validation succesful")

        if doc.creation_info.creator_comment:
            logger.debug(f"CreatorComment: {doc.creation_info.creator_comment}")
            cisaSBOMTypes = ["design", "source", "build", "analyzed", "deployed", "runtime"]

            match = re.search(r':\s*(\w+)', doc.creation_info.creator_comment.lower().strip())
            sbom_type = None
            if match:
                sbom_type = match.group(1)

            if not sbom_type in cisaSBOMTypes:
                logger.debug(f"CreatorComment ({sbom_type}) is not in the CISA SBOM Type list ({cisaSBOMTypes})")
                problems.append("Invalid CreationInfo", "General", "General", f"CreatorComment ({doc.creation_info.creator_comment}) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)", file)
            else:
                logger.debug(f"CreatorComment ({doc.creation_info.creator_comment}) is in the CISA SBOM Type list ({cisaSBOMTypes})")
        else:
            problems.append("Missing mandatory field from CreationInfo", "General", "General", f"CreatorComment is missing", file)

        if doc.creation_info.creators:
            organisationCorrect = False
            toolCorrect = False
            for creator in doc.creation_info.creators:
                logger.debug(f"Creator: {creator}")
                if re.match(".*Organization.*", str(creator)):
                    logger.debug(f"Creator: Organization found ({creator})")
                    organisationCorrect = True
                # In RECOMMENDED mode, we check there is an hyphen between tool name and version
                # if re.match(".*Tool.*-.*", str(creator)):
                if re.match(".*Tool.*", str(creator)):
                    logger.debug(f"Creator: Tool found with the correct format ({creator})")
                    toolCorrect = True
            if not organisationCorrect:
                problems.append("Missing or invalid field in CreationInfo::Creator", "General", "General", "There is no Creator field with Organization keyword in it", file)
            if not toolCorrect:
                # problems.append("Missing or invalid field in CreationInfo::Creator", "General", "General","There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen", file)
                problems.append("Missing or invalid field in CreationInfo::Creator", "General", "General","There is no Creator field with Tool keyword in it", file)
        else:
            problems.append("Missing mandatory field from CreationInfo", "General", "General", "Creator is missing", file)

        for package in doc.packages:
            logger.debug(f"Package: {package}")
            if not package.version:
                pass
                ### This is already detected during the NTIA check.
                #problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Version field is missing")
            if not package.supplier:
                pass
                ### This is already detected during the NTIA check.
                #problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Supplier field is missing")
            if strict:
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
                                    problems.append("Useless mandatory field from Package", package.spdx_id, package.name, f"purl ({ref.locator}) in the ExternalRef cannot be converted to a downloadable URL", file)
                                else:
                                    logger.debug(f"Strict PURL check is happy {url}")
                    if not purlFound:
                        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "There is no purl type ExternalRef field in the Package", file)
                else:
                    problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "ExternalRef field is missing", file)
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
                            problems.append("Invalid field in Package", package.spdx_id, package.name, f"PackageHomePage field points to a nonexisting page ({package.homepage})", file)
            # Version specifics
            match guide_version:
                case "1.0":
                    if not package.checksums:
                        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "PackageChecksum field is missing", file)
                    if not package.files_analyzed:
                        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "FilesAnalyzed field is missing", file)
                case "1.1":
                    if strict and (not (package.checksums or package.verification_code)):
                        problems.append("Missing mandatory field from Package", package.spdx_id, package.name, "Both PackageChecksum and PackageVerificationCode fields are missing", file)
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
            list_of_referred_sboms, problems = self.referringLogics[referringLogic](self, doc, dir_name, problems)
        else:
            logger.error(f"Referring logic “{referringLogic}” is not in the registered referring logic list {self.getReferringLogicNames()}")
            sys.exit(1)

        for referred_sbom in list_of_referred_sboms:
            self.validate(
                filePath=referred_sbom,
                strict_purl_check=strict_purl_check,
                strict_url_check=strict_url_check,
                functionRegistry=functionRegistry,
                problems=problems,
                referringLogic=referringLogic)
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
                problems.append("NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText, file)
            else:
                problems.append("NTIA validation error", "Cannot be provided", component, problemText, file)

    def __ntiaErrorLogNew(self, components, problems, doc, problemText, file):
        logger.debug(f"# of components: {len(components)}")
        for component in components:
            logger.debug(f"Erroneous component: {component}")
            if len(component) > 1:
                problems.append("NTIA validation error", component[1], component[0], problemText, file)
            else:
                spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
                logger.debug(f"SPDX element: {spdxPackage}")
                if spdxPackage:
                    problems.append("NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText, file)
                else:
                    problems.append("NTIA validation error", "Cannot be provided", component, problemText, file)

def referred_yocto_all(self, doc: Document, dir_name: str, problems: Problems):
    logger.debug("In Yocto all")
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
                    doc_location = f"{doc_location}.spdx.json"
                else:
                    doc_location = f"{dir_name}/{doc_location}.spdx.json"
                logger.debug(f"Document location is: {doc_location}")
                documents.append(doc_location)
    return documents, problems

def referred_yocto_contains_only(self, doc: Document, dir_name: str, problems: Problems):
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

def referred_checksum_all(self, doc: Document, dir_name: str, problems: Problems):
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
                    problems.append("File error", "General", "General", f"Non existing file referenced (Checksum: {algorithm}, {checksum}, Document Ref: {checksums[algorithm][checksum]})", "")
            else:
                logger.error(f"Algorithm not found in Logic Store {algorithm}, {checksum}")

    documents_dd = set()
    documents_dd = [x for x in documents if not (x in documents_dd or documents_dd.add(x))]

    logger.debug(f"documents_dd: {documents_dd}")

    return documents_dd, problems

def referred_none(self, doc: Document, dir_name: str, problems: Problems):
    return [], problems

def _dummy_referred_logic(self, doc: Document, dir_name: str, problems: Problems):
    pass
