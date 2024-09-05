# © 2024 Nokia
# Licensed under the Apache License 2.0
# SPDX-License-Identifier: Apache-2.0

FROM python:3.9.18-bookworm

RUN apt-get update

COPY ./openchain_telco_sbom_validator/cli.py ./cli.py
COPY ./openchain_telco_sbom_validator/validator.py ./validator.py
COPY ./requirements.txt ./requirements.txt
COPY ./entry.sh ./
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "/entry.sh"]
