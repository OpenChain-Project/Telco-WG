# © 2024 Nokia
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

from setuptools import setup

setup(
    name='openchain_telco_sbom_validator',
    version='0.1',    
    description='Validator against version 1 of the OpenChain Telco SBOM Guide',
    url='https://github.com/OpenChain-Project/Telco-WG/tree/main/tools',
    author='Gergely Csatari, Marc-Etienne Vargenau',
    author_email='gergely.csatari@nokia.com, marc-etienne.vargenau@nokia.com',
    license='Apache License 2.0',
    license_files=("LICENSE",),
    packages=['openchain_telco_sbom_validator'],
    install_requires=['spdx-tools>=0.8.2',
                      'requests>=2.32.3',                     
                      'prettytable>=3.11.0', 
                      'packageurl-python>=0.15.6',
                      'ntia-conformance-checker>=3.0.0', 
                      'validators>=0.33.0'],

    entry_points={
    'console_scripts': [
        'open-chain-telco-sbom-validator=openchain_telco_sbom_validator.cli:main'
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Communications :: Telephony",
        "Topic :: Communications",
        'Programming Language :: Python :: 3',
    ],
    zip_safe=True,
)
