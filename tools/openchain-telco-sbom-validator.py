#!/bin/python3

# © 2024 Nokia
# Authors: Gergely Csatári, Marc-Etienne Vargenau
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import sys
import re
import os
import shutil
import json
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

def main():
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='A script to validate an SPDX file against the OpenChain Telco SBOM Guide.')
    # TODO: This should go in without any parameter.
    parser.add_argument('--debug', action="store_true",
                        help='Print debug logs.')
    parser.add_argument('--nr-of-errors',
                        help='Sets a limit on the number of errors displayed')
    parser.add_argument('input',
                        help='The input SPDX file.')
    parser.add_argument('--strict-purl-check', action="store_true",
                        help='Runs a strict check on the given purls. The default behaviour is to run a non strict purl'
                        'check what means that it is not checked if the purl is translating to a downloadable url.')
    parser.add_argument('--strict-url-check', action="store_true",
                        help='Runs a strict check on the URLs of the PackageHomepages. Strict check means that the'
                        ' validator checks also if the given URL can be accessed. The default behaviour is to run a non'
                        ' strict URL check what means that it is not checked if the URL points to a valid page. Strict'
                        'URL check requires access to the internet and takes some time.')

    args = parser.parse_args()

    # print(args)
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging is ON")
    if not args.input:
        logger.error("ERROR! Input is a mandatory parameter.")
        sys.exit(2)
    else:
        logger.info("Input file is " + args.input)
        # TODO: Check if the file exist.

    if args.nr_of_errors:
        if not args.nr_of_errors.isnumeric():
            logger.error(f"nr-of-errors must be a number and not {args.nr_of_errors}")
            sys.exit(1)
    if args.strict_purl_check:
        logger.info("Running strict checks for purls, what means that it is tested if the purls can be translated to a downloadable url.")
    if args.strict_url_check:
        logger.info("Running strict checks for URL, what means that it is tested if the PackageHomePage fields are pointing to real pages.")

    logger.debug("Start parsing")

    filePath = str(args.input);
    try:
        doc = parse_anything.parse_file(str(args.input))
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
    logger.debug("Start validating")

    problems = []

    errors = validate_full_spdx_document(doc)
    if errors:
        logger.error("ERROR! The file is not a valid SPDX file")
        for error in errors:
            logger.debug(f"Validation error: {error.context.parent_id} - {error.context.full_element} - {error.validation_message}")
            spdxId = ""
            name = ""
            if not isinstance(error.context.full_element, type(None)):
                spdxId = error.context.full_element.spdx_id
                name = error.context.full_element.name

            problems.append(["SPDX validation error", f"{spdxId}", f"{name}", f"{error.validation_message}"])

    # Checking against NTIA minimum requirements
    # No need for SPDX validation as it is done previously.
    logger.debug("Start of NTIA validation")
    sbomNTIA = ntia.SbomChecker(filePath, validate=False)
    if not sbomNTIA.ntia_minimum_elements_compliant:
        logger.debug("NTIA validation failed")
        components = sbomNTIA.get_components_without_names()
        ntiaErrorLog(components, problems, doc,"Package without a name")
        components = sbomNTIA.get_components_without_versions(return_tuples=True)
        ntiaErrorLogNew(components, problems, doc,"Package without a version")
        components = sbomNTIA.get_components_without_suppliers(return_tuples=True)
        ntiaErrorLogNew(components, problems, doc,"Package without a package supplier or package originator")
        components = sbomNTIA.get_components_without_identifiers()
        ntiaErrorLog(components, problems, doc,"Package without an identifyer")

    else:
        logger.debug("NTIA validation succesful")

    if doc.creation_info.creator_comment:
        logger.debug(f"CreatorComment: {doc.creation_info.creator_comment}")
        cisaSBOMTypes = ["Design", "Source", "Build", "Analyzed", "Deployed", "Runtime"]

        typeFound = False
        for cisaSBOMType in cisaSBOMTypes:
            logger.debug(f"Checking {cisaSBOMType} against {doc.creation_info.creator_comment} ({doc.creation_info.creator_comment.find(cisaSBOMType)})")
            creator_comment = doc.creation_info.creator_comment.lower();
            if 0 <= creator_comment.find(cisaSBOMType.lower()):
                logger.debug("Found")
                typeFound = True

        if not typeFound:
            problems.append(["Invalid CreationInfo", "General", "General", f"CreatorComment ({doc.creation_info.creator_comment}) is not in the CISA SBOM Type list (https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)"])
    else:
        problems.append(["Missing mandatory field from CreationInfo", "General", "General", f"CreatorComment is missing"])

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
            problems.append(["Missing or invalid field in CreationInfo::Creator", "General", "General", "There is no Creator field with Organization keyword in it"])
        if not toolCorrect:
            problems.append(["Missing or invalid field in CreationInfo::Creator", "General", "General","There is no Creator field with Tool keyword in it or the field does not contain the tool name and its version separated with a hyphen"])
    else:
        problems.append(["Missing mandatory field from CreationInfo", "General", "General", "Creator is missing"])

    for package in doc.packages:
        logger.debug(f"Package: {package}")
        if not package.version:
            problems.append(["Missing mandatory field from Package", package.spdx_id, package.name, "Version field is missing"])
        if not package.supplier:
            problems.append(["Missing mandatory field from Package", package.spdx_id, package.name, "Supplier field is missing"])
        if not package.checksums:
            problems.append(["Missing mandatory field from Package", package.spdx_id, package.name, "Checksum field is missing"])
        if package.external_references:
            purlFound = False
            for ref in package.external_references:
                logger.debug(f"cat: {str(ref.category)}, type: {ref.reference_type}, locator: {ref.locator}")
                if ref.category == ExternalPackageRefCategory.PACKAGE_MANAGER and ref.reference_type == "purl":
                    # Based on https://github.com/package-url/packageurl-python
                    purlFound = True
                    if args.strict_purl_check:
                        url = purl2url.get_repo_url(ref.locator)
                        if not url:
                            logger.debug("Purl (" + ref.locator + ") parsing resulted in empty result.")
                            problems.append(["Useless mandatory field from Package", package.spdx_id, package.name, f"purl ({ref.locator}) in the ExternalRef cannot be converted to a downloadable URL"])
                        else:
                            logger.debug(f"Strict PURL check is happy {url}")
            if not purlFound:
                problems.append(["Missing mandatory field from Package", package.spdx_id, package.name, "There is no purl type ExternalRef field in the Package"])
        else:
            problems.append(["Missing mandatory field from Package", package.spdx_id, package.name, "ExternalRef field is missing"])
        if isinstance(package.homepage, type(None)):
            logger.debug("Package homepage is missing")
        else:
            logger.debug(f"Package homepage is ({package.homepage})")
            if not validators.url(package.homepage):
                logger.debug("Package homepage is not a valid url")
                # Adding this to the problem list is not needed as the SPDX validator also adds it
                # problems.append(["Invalid field in Package", package.spdx_id, package.name, f"PackageHomePage is not a valid url ({package.homepage})"])
            else:
                if args.strict_url_check:
                    try:
                        logger.debug("Checking package homepage")
                        page = requests.get(package.homepage)
                    except Exception as err:
                        logger.debug(f"Exception received ({format(err)})")
                        problems.append(["Invalid field in Package", package.spdx_id, package.name, f"PackageHomePage field points to a nonexisting page ({package.homepage})"])
    if problems:
        if args.nr_of_errors:
            problems = problems[0:int(args.nr_of_errors)]

        resultTable = PrettyTable(align = "l")
        resultTable.padding_width = 1
        resultTable.field_names = ["#", "Error type", "SPDX ID", "Package name", "Reason"]

        # TODO: now Error type and SPDX ID uses more space than Package name and Reason, this should be vice versa
        width = shutil.get_terminal_size().columns
        resultTable._max_width = {"#": 4,
                                  "Error type": int((width - 4)/6),
                                  "SPDX ID": int((width - 4)/6),
                                  "Package name": int((width - 4)/3),
                                  "Reason": int((width - 4)/3)}
        i = 0
        for problem in problems:
            i = i + 1
            resultTable.add_row([i, problem[0], problem[1], problem[2], problem[3]], divider=True)

        print(resultTable)
        print(f"The SPDX file {args.input} is not compliant with the OpenChain Telco SBOM Guide")
        sys.exit(1)
    else:
        print(f"The SPDX file {args.input} is compliant with the OpenChain Telco SBOM Guide")
        sys.exit(0)

def ntiaErrorLog(components, problems, doc, problemText):
    logger = logging.getLogger(__name__)
    logger.debug(f"# of components: {len(components)}")
    for component in components:
        logger.debug(f"Erroneous component: {component}")
        spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
        logger.debug(f"SPDX element: {spdxPackage}")
        if spdxPackage:
            problems.append(["NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText])
        else:
            problems.append(["NTIA validation error", "Cannot be provided", component, problemText])

def ntiaErrorLogNew(components, problems, doc, problemText):
    logger = logging.getLogger(__name__)
    logger.debug(f"# of components: {len(components)}")
    for component in components:
        logger.debug(f"Erroneous component: {component}")
        if len(component) > 1:
            problems.append(["NTIA validation error", component[1], component[0], problemText])
        else:
            spdxPackage = document_utils.get_element_from_spdx_id(doc, component)
            logger.debug(f"SPDX element: {spdxPackage}")
            if spdxPackage:
                problems.append(["NTIA validation error", spdxPackage.spdx_id, spdxPackage.name, problemText])
            else:
                problems.append(["NTIA validation error", "Cannot be provided", component, problemText])

if __name__ == "__main__":
    main()
