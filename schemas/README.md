# Schemas of OpenChain Telco Guide
This directory is an implementation of json schemas of Telco Guide. The file [openchain-telco-guide-v1.0-schema.json](openchain-telco-guide-v1.0-schema.json) is just the json schema file you can take to your project. 

As further described below, a technology viewpoint is shown below how to generate json schema file from scratch if you wanna a clear comprehension of underlying logic.

## SPDX 2.2 and SPDX 2.3
In the specification of OpenChain Telco Guide, we say 'An OpenChain Telco SBOM Guide compatible document SHALL adhere to the version 2.2 of the SPDX Data Format as standardized in ISO/IEC 5962:2021, or to the version 2.3 of the standard'. By 2024-08-05, v2.2, v2.2.1, v2.2.2 and v2.3 have been released in github website. We choose v2.2.2 and v2.3 as origin json schema implementation.

The difference between spdx 2.2 and spdx 2.3 is that spdx 2.3 require less license info. For example, you can see concluded license field in spdx 2.2 [link](https://spdx.github.io/spdx-spec/v2.2.2/package-information/#713-concluded-license-field) and in spdx 2.3 [link](https://spdx.github.io/spdx-spec/v2.3/package-information/#713-concluded-license-field).

In the directory `internal`, you can see four files about spdx json schema. 
- [spdx-v2.2.2-origin-schema.json](internal/spdx-v2.2.2-origin-schema.json)
- [spdx-v2.2.2-fix-schema.json](internal/spdx-v2.2.2-fix-schema.json)
- [spdx-v2.3-origin-schema.json](internal/spdx-v2.3-origin-schema.json)
- [spdx-v2.3-fix-schema.json](internal/spdx-v2.3-fix-schema.json)

The term 'origin' means that the file is copied from official github website. The file [spdx-v2.2.2-origin-schema.json](internal/spdx-v2.2.2-origin-schema.json) comes from [link](https://github.com/spdx/spdx-spec/blob/v2.2.2/schemas/spdx-schema.json). And the file [spdx-v2.3-origin-schema.json](internal/spdx-v2.3-origin-schema.json) comes from [link](https://github.com/spdx/spdx-spec/blob/v2.3/schemas/spdx-schema.json).Also, the v2.2.2 specification can be found in [link](https://spdx.github.io/spdx-spec/v2.2.2/) and the v2.3 specification can be found in [link](https://spdx.github.io/spdx-spec/v2.3/).

The term 'fix' means something has been fixed from the origin files. Why should we do it? There are three main reasons. 

Firstly, do bugfix works. Spdx github project [link](https://github.com/spdx/spdx-spec/) is rapidly developed. Unfortunately, official json schema implementations in SPDX github are not consistent with official SPDX specifications. To confirm this, a [json_schema_compare.py](internal/json_schema_compare.py) script is developed. The comparison between SPDX v2.2.2 origin and fix one can be shown below.

```
internal $ python3 json_schema_compare.py -f spdx-v2.2.2-origin-schema.json spdx-v2.2.2-fix-schema.json 
{
    "field_mandatory_comparison": {
        "more_fields": [
            "doc(object)->snippets(array)->snippets_item(object)->name"
        ],
        "less_fields": [
            "doc(object)->documentNamespace",
            "doc(object)->creationInfo(object)->creators",
            "doc(object)->files(array)->files_item(object)->checksums",
            "doc(object)->files(array)->files_item(object)->licenseInfoInFiles",
            "doc(object)->snippets(array)->snippets_item(object)->ranges"
        ]
    },
    "field_existence_comparison": {}
}
```
In SPDX 2.2.2 specifications, `name` field in `snippets` in not mandatory, while in SPDX 2.2.2 json schema implementation is mandatory. And field `documentNamespace`, field `checksums` in `files`, field `licenseInfoInFiles` in `files` and field `ranges` in `snippets` is mandatory in SPDX 2.2.2 specifications, while not mandatory in json schema implementation. It is the same to SPDX 2.3 version. The bugfixes for spdx have been pulled request to official github project.

Secondly, it is impossible to reuse SPDX 2.2.2/2.3 json schema implementation in Telco Guide because declarations of `"additionalProperties": false` exist in it, which means you cannot extend any other field. So the fix one will omit this declaration to extend more fields.

Thirdly, arrange order of fields in implementation according to order of fields in official specifications to make implementation more human-readable. In origin json schema implementation of SPDX, orders of fields are in a messy.

## Openchain Telco Guide JSON Schema
SPDX 2.2 and SPDX 2.3 are not compatible!
```
internal $ python3 json_schema_compare.py -f spdx-v2.3-fix-schema.json spdx-v2.2.2-fix-schema.json 
{
    "field_mandatory_comparison": {
        "less_fields": [
            "doc(object)->files(array)->files_item(object)->copyrightText",
            "doc(object)->files(array)->files_item(object)->licenseConcluded",
            "doc(object)->files(array)->files_item(object)->licenseInfoInFiles",
            "doc(object)->packages(array)->packages_item(object)->copyrightText",
            "doc(object)->packages(array)->packages_item(object)->licenseConcluded",
            "doc(object)->packages(array)->packages_item(object)->licenseDeclared",
            "doc(object)->snippets(array)->snippets_item(object)->copyrightText",
            "doc(object)->snippets(array)->snippets_item(object)->licenseConcluded"
        ]
    },
    "field_existence_comparison": {
        "more_fields": [
            "doc(object)->packages(array)->packages_item(object)->builtDate(string)",
            "doc(object)->packages(array)->packages_item(object)->primaryPackagePurpose(string)",
            "doc(object)->packages(array)->packages_item(object)->releaseDate(string)",
            "doc(object)->packages(array)->packages_item(object)->validUntilDate(string)"
        ]
    }
}
```
SPDX 2.3 add four fields that are all not mandatory in comparison with SPDX 2.2 and require less license info mandatory fields. This means if it meets SPDX 2.3, it will meet SPDX 2.2. So we choose SPDX 2.3 as a base implementation of Telco Guide. Then we add `MUST` feild in Telco Guide which can be shown below.
```
internal $ python3 json_schema_compare.py -f ../openchain-telco-guide-v1.0-schema.json spdx-v2.3-fix-schema.json 
{
    "field_mandatory_comparison": {
        "more_fields": [
            "doc(object)->packages(array)->packages_item(object)->copyrightText",
            "doc(object)->packages(array)->packages_item(object)->licenseConcluded",
            "doc(object)->packages(array)->packages_item(object)->licenseDeclared",
            "doc(object)->packages(array)->packages_item(object)->supplier",
            "doc(object)->packages(array)->packages_item(object)->version"
        ]
    },
    "field_existence_comparison": {
        "more_fields": [
            "doc(object)->packages(array)->packages_item(object)->version(string)"
        ]
    }
}
```
The difference between Telco Guide and SPDX 2.3 can be shown below.
- The field `version` in field `packages` is added into Telco Guide. 
- The field `copyrightText`, `licenseConcluded`, `licenseDeclared`, `supplier`, `version` in field `packages` is declared as mandatory. 
- add descriptions into some fields json schema.
- Revise `$id` and `title`.