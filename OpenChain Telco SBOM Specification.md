
# OpenChain Telecommunications Group SBOM Specification [Draft v 1.0]

## 1.	Scope

This document aims to outline certain requirements related to how an entity creates, delivers, and consumes Software Bill of Materials (SBOM), so that entities that produce and/or consume SBOMs that conform to this specification can ensure repeatability and streamlining of tools and processes for generating and consuming SBOMs. *Please Note* that this specification does not require a conforming entity to adopt OpenChain (in any version) but doing so is greatly encouraged. 

Conformance to this specification is done on a per SBOM level: an entity can adopt the specification as its sole way of delivering SBOMs but it’s the individual SBOM that is conformant to the specification, not the entity that provides the SBOM.  

Releasing SBOMs conforming to this specification does not preclude an entity from also delivering SBOMs for the same software in alternate ways or formats, but those SBOMs are not conformant to the specification, thus neither an entity nor a software product is conformant to the specification as only the SBOM can be conformant to the specification.

This specification is licensed under [Creative Commons Attribution License 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/).

## 2.	Terms and definitions
### Data Format

Data Format means the data format of the information in the SBOM. Possible Data Formats include SPDX, Cyclone DX, SWID, or other proprietary formats.
### Entity: 
Entity shall mean the the legal entity (for profit, non profit, or natural person) that distributes software to third parties (e.g., other organizations or individuals). Entity does not include other group companies, or companies under common control of the Entity. 
### SBOM: 

A Software Bill of Materials (SBOM) is a formal record containing the details and supply chain relationships of various components used in building software.

### SPDX
SPDX (Software Package Data Exchange) is the [ISO standard](https://www.iso.org/standard/81870.html) (ISO/IEC 5962:2021) for exchanging SBOM for a given software package, including associated license and copyright information. The standard was created by the [Linux Foundation's SPDX project](https://spdx.dev/).
### OpenChain
OpenChain means [OpenChain ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html), the international standard that specifies the key requirements of a quality open source license compliance program in order to provide a benchmark that builds trust between organizations exchanging software solutions that incorporate open source software. The OpenChain standard is produced by the [OpenChain project](https://www.openchainproject.org) of the Linux Foundation.

### Transitive dependencies
Transitive dependencies are all components that are necessary for the software to run.  They include direct dependencies, the dependencies of these dependencies, the dependencies of the latter, and so on.

## 3.	Requirements

### 3.3	Data Format 
A Telco Standard SBOM shall adhere to the version 2.2 of the SPDX Data Format as standardized in ISO/IEC 5962:2021 and as further described below with respect to the included elements. 

#### 3.3.1	Verification material/reference material
ISO/IEC 5962:2021 Information technology — SPDX® Specification V2.2.1 https://standards.iso.org/ittf/PubliclyAvailableStandards/c081870_ISO_IEC_5962_2021(E).zip

#### 3.3.2	Rationale 
To ensure simplified handling and streamlining of tooling and competences in the telecommunications supply chain, both for suppliers and consumers of software, a telco standard SBOM  shall adhere to the SPDX Data Format as standardized in ISO/IEC 5962:2021. By harmonizing on the use of this standard SBOM Data Format in an organization's external interfaces, the complexities for organizations supplying and consuming software are simplified, as only one set of unified requirements will be applicable. 
As clarification, an entity is free to use alternative Data Formats for internal use, or deliver SBOMs in alternative Data Formats to organizations that so request or on its own initiative. The Telco Group SBOM specification is a SBOM-level specification to adhere to, and not an organizational specification to adhere to. There are no conforming entities, only conforming SBOMs, delivered by entities that have implemented the Telco SBOM specification.  

### 3.4	SPDX Elements to be included in the SBOM 
Do we take a minimalist approach, do we require ONLY a pre defined set of SPDX elements, or see that as a “lower” limit.  

**Define the elements beyond NTIA *minimum elements of an SBOM* that should be included in the Telco SBOM**
#### 3.4.1	Verification Material/Reference material
NTIA minimum elements https://www.ntia.doc.gov/report/2021/minimum-elements-software-bill-materials-sbom

#### 3.4.2	Rationale
Recognizing the Telco industry need for harmonization and special requirements, possibly beyond the NTIA minimum elements, the "Telco Profile of SPDX" is proposed to ensure predictability to the industry as to the elements of an SBOM that is expected. 

### 3.5	Machine Readable Data Format
The Telco Standard SBOM will include, at a minimum, SPDX in the following machine readable Data Format as default: Tag/Value

#### 3.5.1	Verification material/reference material
#### 3.5.2	Rationale
To facilitate a simplified toolchain, a machine readable version of the SBOM needs to be included. To ensure repeatability and harmonization a conformant SBOM must be in the Tag/Value format. An entity can release additional machine readable Data Formats but they are not required to conform to the Telco SBOM specification.
#### 3.6	Human Readable Data Format
A Telco Standard SBOM will include, at a minimum, the SPDX in the following human readable Data Format as default: Tag/Value
#### 3.6.1	Verification Material/reference material
#### 3.6.2	Rationale 
As the Tag/Value format is also human readable it has been chosen so that both the requirements for a standardized Machine readable and Human Readable version can be met using one file. An entity can release additional human readable Data Formats but they are not required to conform to the Telco SBOM specification. 

### 3.7	SBOM Build information 
SBOMs conforming to the Telco SBOM Specification needs to contain information as they when they were created, both when in time (using the SPDX information) as well as if they were built “pre-build”, “build-time” or “post-build” (also deployment), and to which version of the software they were created (Do we also want to standardize how to convey this information?)    
(Do we instead mandate the time of the SBOM, mandate post build.)
### 3.8	Timing of SBOM delivery
The SBOM shall be delivered no later than at the time of the delivery of the software (in either binary or source form). 

#### 3.8.1	Verification/reference material
#### 3.8.2	Rationale
To ensure that the receiving entity can ingest the software and its SBOM, it shall be delivered no later than at the delivery of the software. An SBOM may be delivered before the software if an adopting entity so elects, but the software delivery must nevertheless be accompanied by the corresponding SBOM to ensure compliance with the specification. 

### 3.9	Method of SBOM delivery
The SBOM shall be embedded into the software “package” where technically feasible. If it is not technically feasible to embed the SBOM into the software “package” being delivered, such as in the case of space-constrained embedded systems, the supplying party will supply a web hosted version of the SBOM that is available for at least X years and shall not in any way restrict recipients’ ability to copy and store these locally for their own use. This include any restrictions placed on the recipient in additional confidentiality agreements.
#### 3.9.1	Verification Material/Reference material
#### 3.9.2	Rationale
Other options of SBOM delivery such as webhosting are less stable and access is not guaranteed over time; however “embedding” may not be technically feasible. Thus, in scenarios where it is not possible on technical grounds to include the SBOM in the software delivery, publishing the SBOM online is permitted provided that: 
### 3.10	SBOM Scope 

***All software vs Open Source software?
Build time only or run time dependencies included as well?
	-Possible to have both in the same SBOM?***

#### 3.10.1	Verification Material/Reference material
#### 3.10.2	Rationale
### 3.11	SBOM in a SaaS deployment
As the Telco SBOM specification is only applied on the SBOM level, there is no requirement on an entity that have elected to supply Telco SBOM specification conformant SBOMs for some or even all of its software deliveries to also provide this for its SaaS offerings. However, an entity may elect to apply the Telco SBOM specification also to its SaaS offerings and thus also deliver the open source software used in the SaaS offerings with their transitive dependencies as an SBOM.

#### 3.11.1	Verification Material/Reference material
#### 3.11.2	Rationale
### 3.12	SBOMs for containers
SBOMs for containers should include all open source components delivered in the container. This includes the packages installed into the container, components copied or downloaded to the container and dependencies used to build the compiled components in the container.

#### 3.12.1	Verification Material/Reference material
#### 3.12.2	Rationale
Every open source component delivered should be part of the SBOMs.

### 3.13	SBOM Verification
Defer to OpenChain security.

#### 3.13.1	Verification Material/Reference material
#### 3.13.2	Rationale
While the verification of SBOMs is an important topic, OpenChain Telco defers this work to other initiatives for the moment and intends to revisit this topic in future iterations of this working document. 
### 3.14	SBOM Merger
SBOMs following this specification can be built from several SBOM files with a well-defined relationship to each other using the relationship definition features in SPDX.

#### 3.14.1	Verification Material/Reference material
#### 3.14.2	Rationale

### 3.15	SBOM Confidentiality
SBOMs may be subject to confidentiality agreements. A conformant SBOM must, however, not be subject to any confidentiality agreements that would prevent a recipient from redistributing the parts of the SBOM applicable to software that such recipient has a right to redistribute.

#### 3.15.1	Verification Material/Reference material
#### 3.15.2	Rationale
Some open source software licenses enable any recipient to redistribute the software. In these situations, the recipients should be also able to redistribute the relevant parts of the SBOMs.

## 4.	Conformant notice: 
To indicate that the software has a conformant SBOM available, you may use the following statement: “Lorem IPSUM"
