FROM python:3.9.18-bookworm

RUN apt-get update

COPY ./openchain-telco-sbom-validator.py ./openchain-telco-sbom-validator.py
COPY ./requirements.txt ./requirements.txt
COPY ./entry.sh ./
RUN pip install -r requirements.txt
ENTRYPOINT ["bash", "/entry.sh"]
