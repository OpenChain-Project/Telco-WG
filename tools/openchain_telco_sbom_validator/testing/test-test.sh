#! /usr/bin/env bash
# -*- coding: utf-8 -*-

# © 2024 Nokia
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

source bash_test_tools

# Documentation is here: https://thorsteinssonh.github.io/bash_test_tools/

function setup
{
   . ../.env/bin/activate
   pip3 install -e ../
}

function teardown
{
    deactivate
}

function test_no_supplier_no_checksum
{
    echo "Test: test_no_supplier_no_checksum"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py test-sbom-01.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "libldap-2.4-2 | Checksum field is missing"
    assert_output_contains "The SPDX file test-sbom-01.spdx is not compliant with the OpenChain Telco SBOM Guide"
}

function test_no_name_no_version_no_supplier
{
    echo "Test: test_no_name_no_version_no_supplier"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py test-sbom-02.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "Package without a name"
    assert_output_contains "golang.org/x/sync-empty-  | Package without a package"
    assert_output_contains "golang.org/x/sync-        | Package without a package"
    assert_output_contains "golang.org/x/sync-empty-  | Checksum field is missing"
    assert_output_contains "golang.org/x/sync-        | Checksum field is missing"
    assert_output_contains "The SPDX file test-sbom-02.spdx is not compliant with the OpenChain Telco SBOM Guide"
}


function test_no_homepage_open_chain_offline
{
    echo "Test: test_no_homepage_open_chain_offline"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py test-sbom-03.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "Empty        | homepage must be a valid"
    assert_output_contains "InvalidURL   | homepage must be a valid"
    assert_output_contains "The SPDX file test-sbom-03.spdx is not compliant with the OpenChain Telco SBOM Guide"
}

function test_no_homepage_open_chain_online
{
    echo "Test: test_no_homepage_open_chain_online"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-03.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "Empty                     | homepage must be a valid"
    assert_output_contains "InvalidURL                | homepage must be a valid"
    assert_output_contains "CorrectFormatIncorrecttar | PackageHomePage field"
    assert_output_contains "The SPDX file test-sbom-03.spdx is not compliant with the OpenChain Telco SBOM Guide"
}

function test_invalid_creator_comment
{
    echo "Test: test_invalid_creator_comment"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-04.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "General       | CreatorComment (No CISA"
    assert_output_contains "The SPDX file test-sbom-04.spdx is not compliant with the OpenChain Telco SBOM Guide"
}

function test_no_creator_comment
{
    echo "Test: test_no_creator_comment"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-05.spdx"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "General       | CreatorComment is missing"
    assert_output_contains "The SPDX file test-sbom-05.spdx is not compliant with the OpenChain Telco SBOM Guide"
}

function test_no_version_json
{
    echo "Test: test_no_version_json"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-06.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "scanoss/engine | Package without a version"
    assert_output_contains "The SPDX file test-sbom-06.spdx.json is not compliant with the OpenChain Telco SBOM Guide"
}

function test_ok_json
{
    echo "Test: test_ok_json"
    run "python3 ../src/openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-07.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_success
    assert_has_output
    assert_output_contains "The SPDX file test-sbom-07.spdx.json is compliant with the OpenChain Telco SBOM Guide"
}

function test_cli_empty
{
    echo "Test: test_cli_empty"
    run "openchain-telco-sbom-validator"
    assert_terminated_normally
    assert_exit_fail
    assert_has_error
    assert_error_contains "ERROR! Input is a mandatory parameter."
}

function test_cli_version
{
    echo "Test: test_cli_version"
    run "openchain-telco-sbom-validator --version"
    echo "$output"
    assert_terminated_normally
    assert_exit_success
    assert_has_output
    assert_output_contains "OpenChain Telco SBOM Validator version"
}

function test_linked_no
{
    echo "Test: test_linked_none"
    run "openchain-telco-sbom-validator linked-sboms-01/linked-sbom-01.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "2 | Missing"
    assert_output_contains "The SPDX file linked-sboms-01/linked-sbom-01.spdx.json is not compliant with the OpenChain Telco SBOM Guide"
}

function test_linked_none
{
    echo "Test: test_linked_none"
    run "openchain-telco-sbom-validator --reference-logic none linked-sboms-01/linked-sbom-01.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "2 | Missing"
    assert_output_contains "The SPDX file linked-sboms-01/linked-sbom-01.spdx.json is not compliant with the OpenChain Telco SBOM Guide"
}

function test_linked_yocto_all
{
    echo "Test: test_linked_none"
    run "openchain-telco-sbom-validator --reference-logic yocto-all linked-sboms-01/linked-sbom-01.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "37 | SPDX"
    assert_output_contains "One or more of the SPDX files linked-sbom-01.spdx.json, alarm.spdx.json, recipe-alarm.spdx.json, runtime-alarm.spdx.json, alarm.spdx.json, recipe-alarm.spdx.json, em-accessories.spdx.json, alignmentpavendors.spdx.json, recipe-alignmentpavendors.spdx.json, runtime-alignmentpavendors.spdx.json, alignmentpavendors.spdx.json, recipe-alignmentpavendors.spdx.json, alps.spdx.json, runtime-alps.spdx.json, kernel-5.15.155-r42.spdx.json, runtime-kernel-5.15.155-r42.spdx.json, kernel-5.15.155-r42.spdx.json are not compliant with the OpenChain Telco SBOM Guide"
}

function test_linked_yocto-contains-only
{
    echo "Test: test_linked_none"
    run "openchain-telco-sbom-validator --reference-logic yocto-contains-only linked-sboms-01/linked-sbom-01.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "10 | Missing"
    assert_output_contains "One or more of the SPDX files linked-sbom-01.spdx.json, alarm.spdx.json, alignmentpavendors.spdx.json, alps.spdx.json are not compliant with the OpenChain Telco SBOM Guide"
}

function test_linked_nonexistent
{
    echo "Test: test_linked_none"
    run "openchain-telco-sbom-validator --reference-logic nonexistent linked-sboms-01/linked-sbom-01.spdx.json"
    echo "$output"
    assert_terminated_normally
    assert_exit_fail
    assert_has_output
    assert_output_contains "2 | Missing"
    assert_output_contains "The SPDX file linked-sboms-01/linked-sbom-01.spdx.json is not compliant with the OpenChain Telco SBOM Guide"
}



testrunner