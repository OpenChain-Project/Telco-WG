# OpenChain 通信業界SBOM仕様 [Draft v 1.0]

## 1. スコープ

本ドキュメント "OpenChain 通信業界SBOM仕様 "は、事業体がソフトウェア部品表（SBOM）をどのように作成し、配信し、そして消費するか、に関連する特定の要件を概説することを目的とする。この仕様に準拠するSBOMを生成し消費する事業体、または生成か消費する事業体が、SBOMを生成し消費する際のツールおよびプロセスの再現性と合理性を確保できるようにする。この仕様は、適合する事業体がOpenChainを（どのバージョンでも）採用することを要求するものではないが、採用することが大いに推奨されることに留意されたい。

事業体はSBOMを提供する唯一の方法としてこの仕様を採用できるが、仕様に準拠するのは個々のSBOMであり、SBOMを提供する事業体ではない。この仕様に準拠したSBOMは「Telco SBOM（通信業界SBOM）」と呼ばれる。

この仕様に準拠したSBOMをリリースすることは、事業体が同じソフトウェアのSBOMを別の方法または形式で配信することを妨げない。ただし、それらのSBOMは仕様に準拠していないため、事業体もソフトウェア製品も仕様に準拠していない。

本仕様は、 [Creative Commons Attribution License 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/)の下でライセンスされている。

## 2. 用語と定義

この文書内のキーワード "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY",  "OPTIONAL"は、BCP 14 [[RFC2119]](https://www.ietf.org/rfc/rfc2119.txt) [[RFC8174]](https://www.ietf.org/rfc/rfc8174.txt) に記述されているとおりに解釈される。

### データ形式
データ形式とは、SBOM内の情報のデータ形式を意味する。可能なデータ形式には、SPDX、Cyclone DX、SWID、またはその他の独自形式がある。

### 事業体（訳注：頒布者）
事業体（entity）とは、第三者（他の組織または個人など）にソフトウェアを配布する法人（営利、非営利、または（訳注：法人と対比した）個人）を意味する。事業体には、他のグループ会社、または事業体の共通支配下にある会社は含まれない。

### ソフトウェア部品表
ソフトウェア部品表（SBOM）は、ソフトウェアを構築する際に使用される様々なコンポーネントの詳細とサプライチェーンの関係を含む正式な記録である。

### SBOMタイプ
SBOMは以下のいずれかのタイプである：
* Design,
* Source,
* Build,
* Analyzed,
* Deployed,
* Runtime.

これらのタイプの定義は右記を参照すること。
[CISA document](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf).

### SPDX
SPDX（Software Package Data Exchange）とは、[ISO標準(ISO/IEC 5962:2021)](https://www.iso.org/standard/81870.html)であり、ソフトウェアパッケージのSBOMを交換するための規格であり、関連するライセンスや著作権情報も含まれる。この標準は[Linux Foundation の SPDXプロジェクト](https://spdx.dev/)によって纏められた。

### OpenChain
OpenChainとは [OpenChain ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html)を意味し、オープンソースソフトウェアを組み込んだソフトウェアソリューションを交換する組織間の信頼を構築するベンチマークを提供するために、質の高いオープンソースライセンスコンプライアンスプログラムの主要な要件を規定した国際規格です。 OpenChain標準は、Linux Foundationの [OpenChain project](https://www.openchainproject.org)によって作成されている。

### 相互依存関係
相互依存(transitive dependencies)とは、ソフトウェアの実行に必要なすべての コンポーネントのことである。直接的な依存関係ではないパッケージの依存関係も含まれる。

### パッケージURL(PURL)
パッケージURL(PURL)は、ソフトウェアパッケージを一意に識別するためのデファクトスタンダードです。

## 3. 要求要件

### 3.1 データ形式
通信業界SBOM は、ISO/IEC 5962:2021 で標準化されている SPDX データフォーマットのバージョン 2.2 に準拠し、含まれる要素に関して以下に説明する。

#### 3.1.1 検証と参考資料
ISO/IEC 5962:2021 情報技術 - SPDX® 仕様 V2.2.1

#### 3.1.2 根拠
ソフトウェアの供給者と消費者の両方にとって、電気通信サプライチェーンにおけるツールおよび能力の簡素な取り扱いと合理化を確実にするために、通信業界SBOMは、ISO/IEC 5962:2021で標準化されているSPDXデータ形式に準拠しなければならない。 各組織の対外窓口で、この標準SBOMデータフォーマットを使用することで、ソフトウェアを供給する組織と消費する組織の複雑さが簡素化される。

明確化として、事業体は、内部使用のために代替データ形式を自由に使用することができ、また、要求する組織に対して、あるいは自発的に、代替データ形式でSBOMを提供することができる。 OpenChain 通信業界SBOM仕様は準拠すべきSBOM様であり、準拠すべき組織仕様ではない。（OpenChain 通信業界SBOM仕様に）適合する事業体は存在せず、OpenChain 通信業界SBOM仕様を実装した事業体によって提供された（OpenChain 通信業界SBOM仕様に）適合するSBOMのみが存在する。

### 3.2 通信業界SBOMに含まれるSPDX要素

以下の要素が必須である。

文書作成情報（Document creation information）
* SPDXVersion: SPDXに必須
* DataLicense: SPDXに必須
* SPDXID: SPDXに必須
* DocumentName: SPDXに必須
* DocumentNamespace: SPDXに必須
* Creator: SPDXに必須
* Created: SPDXに必須
* CreatorComment:  “SBOM Build information” に入力できるようにする

パッケージ情報（Package information）
* PackageName: SPDXに必須
* SPDXID: SPDXに必須
* PackageVersion: needed by “NTIA SBOM Minimum elements”
* PackageSupplier: needed by “NTIA SBOM Minimum elements”
* PackageDownloadLocation: SPDXに必須
* FilesAnalyzed
* PackageChecksum:  “NTIA SBOM最小要素” によって推奨
* PackageLicenseConcluded: SPDXに必須
* PackageLicenseDeclared: SPDXに必須
* PackageCopyrightText: SPDXに必須

パッケージはパッケージURL(PURL)によって識別されるべきである。

SPDX要素間の関係
* Relationship: at least DESCRIBES and CONTAINS, needed by “NTIA SBOM Minimum elements”

#### 3.2.1 Verification and reference material
NTIA minimum elements

#### 3.2.2 Rationale
Recognizing the Telco industry need for harmonization and special requirements, possibly beyond the NTIA minimum elements, the “OpenChain Telco SBOM specification” is proposed to ensure predictability to the industry as to the elements of an SBOM that is expected.

“Component Hash” is recommended, but not required by the “NTIA SBOM Minimum elements”.
In SPDX, it maps to PackageChecksum.
We make it mandatory as it is important to uniquely identify a package.
Most SCA tools have the capability to produce hashes.

Package URL (PURL) is a _de facto_ standard to uniquely identify software packages.

### 3.3 Machine Readable Data Format
The Telco SBOM SHALL include, at a minimum, the SPDX in the following machine readable format as default: Tag:Value

#### 3.3.1 Verification and reference material
Tag:Value is described here in SPDX 2.2 https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements

#### 3.3.2 Rationale
There are 3 majors formats for SBOMs: SPDX, CycloneDX, and SWID.
These 3 formats are the ones recommended by NTIA document "The Minimum Elements For a Software Bill of Materials (SBOM)" (see References section).

The reasons for selecting SPDX as data format of the Telco SBOM specification include the following:
* SPDX is an ISO standard,
* SPDX has more features than CycloneDX for license compliance,
* SPDX has a human-readable format (CycloneDX has only JSON and XML),
* SWID is more a software identifier than a fully fledged SBOM format.

To facilitate a simplified toolchain, a machine readable version of the SBOM needs to be included. To ensure repeatability and harmonization a conformant SBOM must be in the Tag:Value format. An entity can release additional machine readable formats but they are not required to conform to the specification.

Tag:Value is the most human-readable format, and there are converters between the various SPDX formats
(e.g. https://tools.spdx.org/app/convert/).

### 3.4 Human Readable Data Format
A Telco SBOM SHALL include, at a minimum, the SPDX in the following human readable format as default: Tag:Value

#### 3.4.1 Verification and reference material
Tag:Value is described here in SPDX 2.2 https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements

#### 3.4.2 Rationale
As the Tag:Value format is also human readable it has been chosen so that both the requirements for a standardized machine readable and human readable version can be met using one file. An entity can release additional human readable formats but they are not required to conform to the OpenChain Telco SBOM specification.

### 3.5 SBOM Build information
SBOMs conforming to the Telco SBOM Specification MUST contain information as when they were created (using the SPDX `Created` field) and to which version of the software they were created (using the SPDX `CreatorComment` field).

The `Creator` field MUST:
* contain a line with the `Organization` keyword;
* contain a line with the `Tool` keyword; in this line we MUST have after the `Tool` keyword the tool name and the tool version.

The tool name and the tool version SHOULD be separated by hyphen ("-"), no other hyphen SHOULD appear on the line.

SBOMs conforming to the Telco SBOM Specification MUST provide their SBOM Type as
[defined by CISA](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)
in the `CreatorComment` field.

#### 3.5.1 Verification and reference material
SPDX standard

#### 3.5.2 Rationale
It is important to know which tool and which version of the tool have created the SBOM.

The SPDX standard gives "toolidentifier-version" as an example, but it is not mandatory to have this syntax.

For example, there is a tool that outputs:
```
Creator: Tool: sigs.k8s.io/bom/pkg/spdx
```
We have also:
```
Creator: Tool: scancode-toolkit 30.1.0
```
and
```
Creator: Tool: SCANOSS-PY: 1.5.1
```
where the name contains an hyphen, and the tool name and tool version are not separated by an hyphen.

So we cannot require a precise syntax.

### 3.6 Timing of SBOM delivery
The SBOM SHALL be delivered no later than at the time of the delivery of the software (in either binary or source form). 

#### 3.6.1 Verification and reference material
“NTIA SBOM Minimum elements”, section “Distribution and Delivery”

#### 3.6.2 Rationale
To ensure that the receiving entity can ingest the software and its SBOM, it shall be delivered no later than at the delivery of the software. An SBOM may be delivered before the software if an adopting entity so elects, but the software delivery must nevertheless be accompanied by the corresponding SBOM to ensure compliance with the specification.

### 3.7 Method of SBOM delivery
The SBOM SHALL be embedded into the software “package” where technically feasible. If it is not technically feasible to embed the SBOM into the software “package” being delivered, such as in the case of space-constrained embedded systems, the supplying party will supply a web hosted version of the SBOM that is available for at least 18 months and SHALL NOT in any way restrict recipients’ ability to copy and store these locally for their own use. Such restrictions MAY NOT be placed on the recipient in additional confidentiality agreements. 

#### 3.7.1 Verification and reference material
“NTIA SBOM Minimum elements”, section “Distribution and Delivery”

#### 3.7.2 Rationale
Other options of SBOM delivery such as webhosting are less stable and access is not guaranteed over time; however “embedding” may not be technically feasible. Thus, in scenarios where it is not possible on technical grounds to include the SBOM in the software delivery, publishing the SBOM online is permitted provided that the SBOM is accessible for the recipients of the software for 18 months. This duration is in line with the OpenChain specification requirements on recertification.

### 3.8 SBOM Scope
The SBOM SHALL contain all open source software that is delivered with the product including all of the transitive dependencies. The SBOM SHOULD contain all commercial components.

If some components are not included, they MUST be reported as “known unknowns.”

#### 3.8.1 Verification and reference material
“NTIA SBOM Minimum elements”, section “Known Unknowns”

#### 3.8.2 Rationale
It might not be possible, advisable or feasible to have the commercial component information in the SBOM. However, it is advisable that the SBOM should be as complete as possible.

### 3.9 SBOM in a SaaS deployment
As the OpenChain Telco SBOM specification is only applied on the SBOM level, there is no requirement on an entity that have elected to supply a Telco SBOM for some or even all of its software deliveries to also provide this for its SaaS offerings. However, an entity may elect to apply the OpenChain Telco SBOM specification also to its SaaS offerings and thus also deliver the open source software used in the SaaS offerings with their transitive dependencies as an SBOM.

#### 3.9.1 Verification and reference material

#### 3.9.2 Rationale
There is currently no consensus in the industry on what an SaaS SBOM should contain.

### 3.10 SBOMs for containers
SBOMs for containers SHOULD include all open source components delivered in the container. This includes the packages installed into the container, components copied or downloaded to the container and dependencies used to build the compiled components in the container.

#### 3.10.1 Verification and reference material

#### 3.10.2 Rationale
Every open source component delivered should be part of the SBOMs.

### 3.11 SBOM Verification
It is RECOMMENDED to provide a digital signature of the SBOM in order to guarantee the
integrity of the SBOM.

#### 3.11.1 Verification and reference material
Sigstore https://www.sigstore.dev/ is an example of such capability.

#### 3.11.2 Rationale
While the verification of SBOMs is an important topic, OpenChain Telco defers this work to other initiatives for the moment and intends to revisit this topic in future iterations of this document.

### 3.12 SBOM Merger
SBOMs following this specification can be built from several SBOM files with a well-defined relationship to each other using the relationship definition features in SPDX.

#### 3.12.1 Verification and reference material
There exist tools to merge several SBOMs into one, e.g. https://github.com/vmware-samples/sbom-composer

#### 3.12.2 Rationale
It is often easier when dealing with a large software product to provide individual SBOMs of its parts than a single SBOM.

### 3.13 SBOM Confidentiality
SBOMs MAY be subject to confidentiality agreements. A conformant SBOM MUST NOT, however, be subject to any confidentiality agreements that would prevent a recipient from redistributing the parts of the SBOM applicable to software that such recipient has a right to redistribute.

#### 3.13.1 Verification and reference material
“NTIA SBOM Minimum elements”, section “Access Control”

#### 3.13.2 Rationale
Some open source software licenses enable any recipient to redistribute the software. In these situations, the recipients should be also able to redistribute the relevant parts of the SBOMs.

## 4. Conformant notice
To indicate that the software has a conformant SBOM available, you MAY use the following statement: “This software is supplied with an SBOM conformant to the OpenChain Telco SBOM Specification v1.0, the specification is available at https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md”

You MAY at your choosing use the following statement in your Telco Specification conformant SBOM “This SBOM conforms to the OpenChain Telco SBOM specification v1.0 https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md, it is provided to the recipient free of charge, and the recipient is free to redistribute this SBOM to any third party that they distribute the corresponding software to, provided that they have all the necessary right to distribute the software to such third party”

The following statement MAY be used as statement in the RFP document, order document, or contract document when requesting an RFP, purchasing orders, or outsourced development orders from a software vendor or telco system suppliers.
When releasing software, it is REQUIRED to provide an SBOM compliant with the OpenChain Telco SBOM Specification v1.0 for all software released.  This specification is available at "[https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md)”

## 5. References

* SPDX (ISO/IEC 5962:2021)
  * https://spdx.dev/
  * https://www.iso.org/standard/81870.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081870_ISO_IEC_5962_2021(E).zip
* OpenChain (ISO/IEC 5230:2020)
  * https://www.openchainproject.org/
  * https://www.iso.org/standard/81039.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081039_ISO_IEC_5230_2020(E).zip
* The Minimum Elements For a Software Bill of Materials (SBOM) a.k.a. “NTIA minimum elements”
  * https://www.ntia.doc.gov/report/2021/minimum-elements-software-bill-materials-sbom
* Package URL (PURL)
  * https://github.com/package-url/purl-spec

