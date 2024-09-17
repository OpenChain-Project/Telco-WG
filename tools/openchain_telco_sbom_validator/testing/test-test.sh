#! /usr/bin/env bash
# -*- coding: utf-8 -*-

# © 2024 Nokia
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

source bash_test_tools

function setup
{
   . ../.env/bin/activate 
}

function teardown
{
    deactivate
}

function test_no_supplier_no_checksum
{
    echo "Test: test_no_supplier_no_checksum"
    run "python3 ../openchain_telco_sbom_validator/cli.py test-sbom-01.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "libldap-2.4-2 | Supplier field is missing"
    assert_output_contains "libldap-2.4-2 | Checksum field is missing"
}

function test_no_name_no_version_no_supplier
{
    echo "Test: test_no_name_no_version_no_supplier"
    run "python3 ../openchain_telco_sbom_validator/cli.py test-sbom-02.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "Package without a name"
    assert_output_contains "golang.org/x/sync | Package without a version"
    assert_output_contains "golang.org/x/sync | Package without a package"
    assert_output_contains "libldap-2.4-2     | Supplier field is missing"
    assert_output_contains "golang.org/x/sync | Version field is missing"
    assert_output_contains "golang.org/x/sync | Version field is missing"
    assert_output_contains "golang.org/x/sync | Supplier field is missing"
    assert_output_contains "golang.org/x/sync | Checksum field is missing"
}


function test_no_homepage_open_chain_offline
{
    echo "Test: test_no_homepage_open_chain_offline"
    run "python3 ../openchain_telco_sbom_validator/cli.py test-sbom-03.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "Empty        | homepage must be a valid"
    assert_output_contains "InvalidURL   | homepage must be a valid"
}

function test_no_homepage_open_chain_online
{
    echo "Test: test_no_homepage_open_chain_online"
    run "python3 ../openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-03.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "Empty                     | homepage must be a valid"
    assert_output_contains "InvalidURL                | homepage must be a valid"
    assert_output_contains "CorrectFormatIncorrecttar | PackageHomePage field"
}

function test_invalid_creator_comment
{
    echo "Test: test_invalid_creator_comment"
    run "python3 ../openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-04.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "General       | CreatorComment (No CISA"
}

function test_no_creator_comment
{
    echo "Test: test_no_creator_comment"
    run "python3 ../openchain_telco_sbom_validator/cli.py --strict-url-check test-sbom-05.spdx"
    echo "$output"
    assert_fail
    assert_has_output
    assert_has_error
    assert_output_contains "General       | CreatorComment is missing"
}    


testrunner