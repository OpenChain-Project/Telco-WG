# OpenChain Telco SBOM 가이드 버전 1.1

## 1. 적용 범위

본 문서 “OpenChain Telco SBOM 가이드”는 조직이 Software Bill of Materials(SBOM, 소프트웨어 자재 명세서)를 생성, 제공, 소비하는 방식과 관련된 특정 요구사항을 개략적으로 제시하는 것을 목적으로 합니다. 본 가이드에 부합하는 SBOM을 생산·소비하는 조직은 SBOM 생성 및 활용을 위한 도구와 프로세스의 반복성과 효율성을 보장할 수 있습니다. 참고: 본 가이드는 준수하는 조직이 OpenChain(어떠한 버전이든)을 반드시 채택할 것을 요구하지 않으나, 채택을 적극 권장합니다.

이 가이드는 개별 SBOM 단위로 적용됩니다. 즉, 조직이 SBOM을 제공하는 유일한 방식으로 본 가이드를 사용할 수 있지만, 본 가이드가 지칭하는 대상은 SBOM을 제공하는 조직이 아니라 각각의 SBOM입니다. 본 가이드를 적용하여 작성된 SBOM은 “OpenChain Telco SBOM Guide Compatible” SBOM으로 불릴 수 있습니다.

본 가이드의 요구사항을 충족하는 SBOM을 공개한다고 해서, 동일한 소프트웨어에 대해 다른 방식이나 포맷의 SBOM을 추가로 제공하는 것이 제한되지는 않습니다.

이 가이드는 [Creative Commons Attribution License 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/) 라이선스로 배포됩니다.

## 2. 용어 및 정의

본 문서에서 사용되는 "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", "OPTIONAL" 등의 용어는, 모두 대문자로 표기된 경우에 한해 BCP 14 [[RFC2119]](https://www.ietf.org/rfc/rfc2119.txt) [[RFC8174]](https://www.ietf.org/rfc/rfc8174.txt)에서 정의된 바에 따라 해석되어야 합니다.

### 데이터 포맷
데이터 포맷(Data Format)이란 SBOM 내 정보의 데이터 형식을 의미합니다. 사용 가능한 데이터 포맷에는 SPDX, Cyclone DX, SWID 또는 기타 독점 포맷이 포함될 수 있습니다.

### Entity(엔터티, 조직)

Entity(엔터티)란 소프트웨어를 제3자(예: 다른 조직 또는 개인)에게 배포하는 법인(영리, 비영리 또는 자연인)을 의미합니다. 단, Entity에는 다른 그룹 계열사나, Entity와 동일한 지배를 받는 회사는 포함되지 않습니다.

### SBOM(Software Bill of Materials, 소프트웨어 자재 명세서)

SBOM(Software Bill of Materials)은 소프트웨어를 구성하는 다양한 컴포넌트의 세부 정보와 공급망 관계를 공식적으로 기록한 문서입니다.

### SBOM Type(SBOM 유형)

SBOM은 다음 중 하나의 유형이 될 수 있습니다:
* Design,
* Source,
* Build,
* Analyzed,
* Deployed,
* Runtime.

각 유형의 정의는 [CISA 문서](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)에서 확인할 수 있습니다.

### SPDX

SPDX(Software Package Data Exchange)는 소프트웨어 패키지의 SBOM(소프트웨어 자재 명세서) 교환을 위한 [ISO 표준](https://www.iso.org/standard/81870.html)(ISO/IEC 5962:2021)입니다. 라이선스 및 저작권 정보도 함께 포함할 수 있습니다. 이 표준은 [Linux Foundation의 SPDX 프로젝트](https://spdx.dev/)에서 개발되었습니다.

### OpenChain

OpenChain이란 [OpenChain ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html)을 의미하며, 오픈소스 소프트웨어가 포함된 소프트웨어 솔루션을 교환하는 조직 간 신뢰 구축을 위해, 고품질 오픈소스 라이선스 컴플라이언스 프로그램의 주요 요구사항을 정의한 국제 표준입니다. OpenChain 표준은 Linux Foundation의 [OpenChain 프로젝트](https://www.openchainproject.org)에서 개발되었습니다.


### Transitive dependencies(간접 의존성)

Transitive dependencies(간접 의존성)란 소프트웨어가 실행되기 위해 필요한 모든 컴포넌트를 의미하며, 직접적인 의존성이 아닌 패키지의 간접 의존성까지 포함합니다.

### Package URL (PURL)

Package URL(PURL)은 소프트웨어 패키지를 고유하게 식별하기 위한 사실상의 표준(_de facto_ standard)입니다.


## 3. 요구사항

### 3.1 데이터 포맷

OpenChain Telco SBOM Guide Compatible 문서는 ISO/IEC 5962:2021에 따라 표준화된 SPDX Data Format(version 2.2) 또는 표준의 version 2.3을 반드시 준수해야 하며, 포함해야 하는 요소에 대해서는 아래에 추가로 설명합니다.

### 3.1 데이터 포맷

OpenChain Telco SBOM Guide 호환 문서는 **ISO/IEC 5962:2021**로 표준화된 SPDX 데이터 포맷 버전 2.2 또는 표준의 버전 2.3을 반드시 준수해야 하며, 아래에 명시된 필수 요소를 포함해야 합니다.

#### 3.1.1 검증 및 참고 자료

* ISO/IEC 5962:2021 Information technology — SPDX® Specification V2.2.1
* [SPDX Specification V2.3](https://spdx.github.io/spdx-spec/v2.3/)

#### 3.1.2 배경 및 이유

통신 산업 공급망에서 소프트웨어 공급자와 소비자 모두의 도구 및 역량의 단순화와 효율화를 보장하기 위해, OpenChain Telco SBOM Guide Compatible 문서는 ISO/IEC 5962:2021로 표준화된 SPDX Data Format을 준수해야 합니다. 조직의 외부 인터페이스에서 이 표준 SBOM Data Format을 사용함으로써, 소프트웨어를 공급·소비하는 조직의 복잡성이 단일 통합 요구사항 세트만 적용되도록 간소화됩니다.

추가 설명으로, 조직은 내부적으로 다른 Data Format을 자유롭게 사용할 수 있으며, 요청이 있거나 자체 판단에 따라 다른 Data Format의 SBOM을 제공할 수도 있습니다. OpenChain Telco SBOM Guide는 SBOM 단위의 Specification이며, 조직 단위의 Specification이 아닙니다. 즉, 준수 조직이 있는 것이 아니라, OpenChain Telco SBOM Guide를 적용하여 제공되는 준수 SBOM이 있을 뿐입니다.

### 3.2 OpenChain Telco SBOM Guide Compatible 문서에 포함되어야 하는 SPDX 요소

다음 요소들은 **필수(REQUIRED)** 입니다.

#### 문서 생성 정보

- SPDXVersion: SPDX에서 필수(mandatory)
- DataLicense: SPDX에서 필수
- SPDXID: SPDX에서 필수
- DocumentName: SPDX에서 필수
- DocumentNamespace: SPDX에서 필수
- Creator: SPDX에서 필수
- Created: SPDX에서 필수
- CreatorComment: “SBOM Build information” 기재 가능

#### 패키지 정보

- PackageName: SPDX에서 필수
- SPDXID: SPDX에서 필수
- PackageVersion: “NTIA SBOM Minimum elements”에서 요구
- PackageSupplier: “NTIA SBOM Minimum elements”에서 요구
- PackageDownloadLocation: SPDX에서 필수
- PackageLicenseConcluded: SPDX 2.2에서 필수
- PackageLicenseDeclared: SPDX 2.2에서 필수
- PackageCopyrightText: SPDX 2.2에서 필수

One of the two attributes PackageChecksum or PackageVerificationCode is RECOMMENDED:
recommended by “NTIA SBOM Minimum elements”

A package SHOULD be identified by a Package URL (PURL).

If the PURL is present, it SHOULD be put in ExternalRef field, e.g.
```
ExternalRef: PACKAGE-MANAGER purl pkg:pypi/django@1.11.1
```

다음 두 속성 중 하나(PackageChecksum 또는 PackageVerificationCode)는 **권장(RECOMMENDED)** 사항입니다(“NTIA SBOM Minimum elements”에서 권장): 

패키지는 **Package URL (PURL)** 로 식별하는 것이 **권장(SHOULD)** 됩니다.

PURL이 존재하는 경우, ExternalRef 필드에 기재하는 것이 좋습니다. 예시:

```
ExternalRef: PACKAGE-MANAGER purl pkg:pypi/django@1.11.1
```


SPDX elements 간의 Relationships

- Relationship: 최소한 DESCRIBES(설명)와 CONTAINS(포함) 관계는 반드시 포함되어야 하며, 이는 “NTIA SBOM Minimum elements”에서 요구하는 사항입니다.

#### 3.2.1 검증 및 참고 자료

- NTIA minimum elements

#### 3.2.2 배경 및 이유

통신 산업의 표준화 및 특수 요구사항을 반영하기 위해, “OpenChain Telco SBOM Guide”는 산업계가 기대하는 SBOM 요소의 예측 가능성을 보장하고자 제안되었습니다.

“Component Hash”는 “NTIA SBOM Minimum elements”에서 필수는 아니지만, 권장(RECOMMENDED)됩니다.

SPDX에서는 해당 항목이 PackageChecksum 또는 PackageVerificationCode에 해당합니다.  
대부분의 SCA(Software Composition Analysis) 도구는 해시 값을 생성할 수 있습니다.

CISA 문서 "Framing Software Component Transparency: Establishing a Common Software Bill of Materials (SBOM), Third Edition"  
https://www.cisa.gov/resources-tools/resources/framing-software-component-transparency-2024  
에서는 두 방식 모두 허용하고 있습니다(2.5절의 표 참조).

Package URL (PURL)은 소프트웨어 패키지를 고유하게 식별하는 사실상의 표준(_de facto_ standard)입니다.


### 3.3 기계 판독 가능 데이터 포맷

OpenChain Telco SBOM Compatible 문서는 최소한 다음 중 하나의 기계 판독 가능(Machine Readable) 포맷으로 SPDX를 반드시(SHALL) 포함해야 합니다: Tag:Value 또는 JSON.


#### 3.3.1 검증 및 참고 자료

Tag:Value 및 JSON 포맷에 대한 설명은 아래에서 확인할 수 있습니다:  
* SPDX 2.2: https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements  
* SPDX 2.3: https://spdx.github.io/spdx-spec/v2.3/conformance/#44-standard-data-format-requirements

#### 3.3.2 배경 및 이유

SBOM에는 대표적으로 3가지 주요 포맷이 있습니다: SPDX, CycloneDX, SWID.  
이 세 가지 포맷은 NTIA 문서 "The Minimum Elements For a Software Bill of Materials (SBOM)"(참고문헌 섹션 참조)에서 권장하는 포맷입니다.

OpenChain Telco SBOM Guide의 데이터 포맷으로 SPDX를 선택한 이유는 다음과 같습니다:
* SPDX는 ISO 표준입니다.
* SPDX는 라이선스 컴플라이언스 측면에서 CycloneDX보다 더 많은 기능을 제공합니다.
* SPDX는 사람이 읽을 수 있는(human-readable) 포맷을 제공합니다(CycloneDX는 JSON과 XML만 지원).
* SWID는 완전한 SBOM 포맷이라기보다는 소프트웨어 식별자에 가깝습니다.


To facilitate a simplified toolchain, a machine readable version of the SBOM needs to be included. To ensure repeatability and harmonization a conformant SBOM must be in Tag:Value or JSON format. An entity can release additional machine readable formats but they are not required to conform to the Guide.

Tag:Value is the most human-readable format, and there are converters between the various SPDX formats
(e.g. https://tools.spdx.org/app/convert/). JSON is a format produced by several tools.


툴체인의 단순화를 위해서는 기계 판독 가능한 버전의 SBOM이 반드시 포함되어야 합니다.  반복성과 표준화된 활용을 보장하기 위해, 준수하는 SBOM은 반드시 Tag:Value 또는 JSON 포맷이어야 합니다.  조직은 추가적인 기계 판독 가능 포맷으로 SBOM을 제공할 수 있으나, 이는 본 가이드의 준수 요건에 해당하지 않습니다.

Tag:Value는 사람이 읽기에 가장 쉬운(human-readable) 포맷이며, 다양한 SPDX 포맷 간 변환 도구도 존재합니다  
(예: https://tools.spdx.org/app/convert/).  JSON은 여러 도구에서 생성되는 포맷입니다.


### 3.4 Human Readable Data Format
An OpenChain Telco SBOM Compatible document SHALL include, at a minimum, the SPDX in one of the following human readable formats: Tag:Value or JSON.

#### 3.4.1 Verification and reference material
Tag:Value and JSON formats are described here:
* in SPDX 2.2 https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements
* in SPDX 2.3 https://spdx.github.io/spdx-spec/v2.3/conformance/#44-standard-data-format-requirements

#### 3.4.2 Rationale
As the Tag:Value format is also human readable it has been chosen so that both the requirements for a standardized machine readable and human readable version can be met using one file. An entity can release additional human readable formats but they are not required to conform to the OpenChain Telco SBOM Guide.


### 3.4 사람이 읽을 수 있는 데이터 포맷

OpenChain Telco SBOM Compatible 문서는 최소한 다음 중 하나의 사람이 읽을 수 있는(human readable) 포맷으로 SPDX를 반드시(SHALL) 포함해야 합니다: Tag:Value 또는 JSON.

#### 3.4.1 검증 및 참고 자료

Tag:Value 및 JSON 포맷에 대한 설명은 아래에서 확인할 수 있습니다:  
* SPDX 2.2: https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements  
* SPDX 2.3: https://spdx.github.io/spdx-spec/v2.3/conformance/#44-standard-data-format-requirements

#### 3.4.2 배경 및 이유

Tag:Value 포맷은 사람이 읽을 수 있는(human readable) 포맷이기도 하므로, 표준화된 기계 판독 가능 포맷과 사람이 읽을 수 있는 포맷 요구사항을 하나의 파일로 모두 충족할 수 있도록 선택되었습니다.  
조직은 추가적인 사람이 읽을 수 있는 포맷으로 SBOM을 제공할 수 있으나, 이는 OpenChain Telco SBOM Guide의 준수 요건에 해당하지 않습니다.


### 3.5 SBOM 빌드 정보

OpenChain Telco SBOM Guide를 준수하는 SBOM은 반드시(MUST) 생성 시점 정보를 포함해야 하며, 이는 SPDX의 `Created` 필드를 사용하여 명시합니다. 또한 해당 SBOM이 어느 소프트웨어 버전에 대해 생성되었는지의 정보는 SPDX의 `CreatorComment` 필드를 사용하여 기록해야 합니다.

`Creator` 필드에는 반드시(MUST) 다음 내용이 포함되어야 합니다:
* `Organization` 키워드가 포함된 한 줄
* `Tool` 키워드가 포함된 한 줄. 이 줄에는 `Tool` 키워드 뒤에 도구 이름과 도구 버전이 반드시 포함되어야 합니다.

도구 이름과 도구 버전은 하이픈("-")으로 구분하는 것이 요구(SHOULD)되며, 해당 줄에는 다른 하이픈이 포함되지 않는 것이 바람직합니다.

OpenChain Telco SBOM Guide를 준수하는 SBOM은 반드시(MUST)  
[CISA에서 정의한](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)  
SBOM Type을 `CreatorComment` 필드에 제공해야 합니다.

SBOM Type의 권장(RECOMMENDED) 문법은 “SBOM Type: xxx”이며, 여기서 “xxx”는 6가지 키워드(“Design”, “Source”, “Build”, “Analyzed”, “Deployed”, “Runtime”) 중 하나입니다.


#### 3.5.1 검증 및 참고 자료

SPDX standard

#### 3.5.2 배경 및 이유

어떤 도구와 어떤 버전의 도구로 SBOM이 생성되었는지 아는 것은 매우 중요합니다.

SPDX standard에서는 “toolidentifier-version”을 예시로 제시하지만, 반드시 이 문법을 따라야 하는 것은 아닙니다.

예를 들어, 다음과 같은 도구 출력이 존재합니다:
```
Creator: Tool: sigs.k8s.io/bom/pkg/spdx
```
또는
```
Creator: Tool: scancode-toolkit 32.3.0
```
또는
```
Creator: Tool: SCANOSS-PY: 1.18.1
```
위 예시처럼 도구 이름에 하이픈이 포함되거나, 도구 이름과 버전이 하이픈으로 구분되지 않을 수도 있습니다.

따라서 엄격한 문법을 강제할 수는 없습니다.

`CreatorComment`는 자유 텍스트 필드입니다.  SPDX 2.2 및 2.3에는 SBOM Type을 위한 별도 필드가 없기 때문에, 이 필드를 활용하여 CISA SBOM Type을 기록합니다. 물론, 이 외의 정보도 자유롭게 기재할 수 있습니다.

특정한 형식은 요구하지 않습니다.  
단, “Design”, “Source”, “Build”, “Analyzed”, “Deployed”, “Runtime” 중 적어도 하나의 단어가 반드시 포함되어야 하며, 대소문자는 구분하지 않습니다.

따라서 아래와 같은 다양한 작성 방식이 모두 유효하며, 첫 번째 예시가 권장 방식입니다:
```
CreatorComment: SBOM Type: Deployed
```
```
CreatorComment: Analyzed
```
```
CreatorComment: This SBOM was created during build phase.


### 3.6 SBOM 제공 시점

SBOM은 소프트웨어(바이너리 또는 소스 형태) 제공 시점과 동시에, 늦어도 그 시점까지는 반드시(SHALL) 제공되어야 합니다.

#### 3.6.1 검증 및 참고 자료

“NTIA SBOM Minimum elements”, “Distribution and Delivery” 섹션

#### 3.6.2 배경 및 이유

수신 조직이 소프트웨어와 SBOM을 함께 수령하고 활용할 수 있도록, SBOM은 소프트웨어 제공 시점과 동시에, 늦어도 그 시점까지는 반드시 제공되어야 합니다.  
만약 소프트웨어를 도입하는 조직이 원한다면, 소프트웨어 제공 이전에 SBOM을 전달할 수도 있습니다.  
그러나 본 가이드의 준수를 위해서는, 소프트웨어 제공 시 반드시 해당 SBOM이 함께 제공되어야 합니다.

### 3.7 SBOM 제공 방식

SBOM은 기술적으로 가능하다면 소프트웨어 “패키지” 내에 반드시(SHALL) 포함(임베드)되어야 합니다. 만약 임베딩이 기술적으로 불가능한 경우(예: 저장 공간이 제한된 임베디드 시스템 등), 공급자는 SBOM을 최소 18개월 이상 접근 가능한 웹 호스팅 방식으로 제공해야 하며, 수신자가 이를 자신의 용도로 로컬에 복사 및 저장하는 능력을 어떤 방식으로도 제한해서는 아니 됩니다(SHALL NOT). 이러한 제한은 추가적인 비밀유지계약(confidentiality agreement)에서도 수신자에게 부과될 수 없습니다(MAY NOT).

#### 3.7.1 검증 및 참고 자료

“NTIA SBOM Minimum elements”, “Distribution and Delivery” 섹션


#### 3.7.2 배경 및 이유

웹 호스팅 등 SBOM 제공의 다른 옵션은 장기적으로 안정성이 떨어질 수 있고, 지속적인 접근이 보장되지 않을 수 있습니다. 그러나 “임베딩”이 기술적으로 불가능한 경우도 존재합니다. 따라서 소프트웨어 제공 시 SBOM을 패키지 내에 포함하는 것이 기술적으로 불가능하다면, SBOM을 온라인으로 게시하는 것도 허용됩니다. 이 경우, 소프트웨어 수신자가 18개월 동안 SBOM에 접근할 수 있어야 하며, 이 기간은 OpenChain Specification의 재인증 요건과도 일치합니다.


### 3.8 SBOM 범위

SBOM에는 제품과 함께 제공되는 모든 오픈소스 소프트웨어와 그에 포함된 모든 간접 의존성(transitive dependencies)이 반드시(SHALL) 포함되어야 합니다.  
또한, SBOM에는 모든 상용(Commercial) 컴포넌트도 포함하는 것이 요구(SHOULD)됩니다.

일부 컴포넌트가 포함되지 않은 경우, 반드시(MUST) 이를 “known unknowns”(알려진 미포함 항목)로 보고해야 합니다.


#### 3.8.1 검증 및 참고 자료

“NTIA SBOM Minimum elements”, “Known Unknowns” 섹션

#### 3.8.2 배경 및 이유

상용 컴포넌트 정보를 SBOM에 포함하는 것이 불가능하거나 바람직하지 않을 수 있습니다.  그러나 SBOM은 가능한 한 완전하게 작성하는 것이 바람직합니다.

### 3.9 SaaS 환경에서의 SBOM

OpenChain Telco SBOM Guide는 SBOM 단위에만 적용되므로, 조직이 일부 또는 모든 소프트웨어 제공에 대해 OpenChain Telco SBOM Compatible 문서를 제공하기로 선택했더라도, SaaS(Software as a Service) 제공에 대해서까지 이를 반드시 적용해야 할 의무는 없습니다.  그러나 조직이 원한다면, SaaS 제공에도 OpenChain Telco SBOM Guide를 적용하여, SaaS에서 사용되는 오픈소스 소프트웨어와 그 간접 의존성(transitive dependencies)을 SBOM으로 제공할 수 있습니다.


#### 3.9.1 검증 및 참고 자료

(해당 없음)

#### 3.9.2 배경 및 이유

현재 업계에서는 SaaS SBOM에 어떤 내용을 포함해야 하는지에 대한 합의가 없습니다.

### 3.10 컨테이너용 SBOM

컨테이너용 SBOM에는 컨테이너에 포함되어 제공되는 모든 오픈소스 컴포넌트가 포함되어야 하며(SHOULD), 여기에는 컨테이너에 설치된 패키지, 컨테이너에 복사되거나 다운로드된 컴포넌트, 그리고 컨테이너 내에서 빌드된 컴파일 컴포넌트에 사용된 의존성까지 모두 포함됩니다.

#### 3.10.1 검증 및 참고 자료

(해당 없음)

#### 3.10.2 배경 및 이유

제공되는 모든 오픈소스 컴포넌트는 SBOM에 반드시 포함되어야 합니다.


### 3.11 SBOM 검증

SBOM의 무결성을 보장하기 위해 SBOM에 디지털 서명을 제공하는 것이 권장(RECOMMENDED)됩니다.


#### 3.11.1 검증 및 참고 자료

Sigstore https://www.sigstore.dev/ 는 이러한 기능의 예시입니다.

#### 3.11.2 배경 및 이유

SBOM의 검증은 중요한 주제이지만, OpenChain Telco는 현재 이 작업을 다른 이니셔티브에 위임하고 있으며, 향후 본 문서의 개정판에서 이 주제를 다시 다룰 예정입니다.

### 3.12 SBOM 병합

본 가이드를 따르는 SBOM은, SPDX의 관계 정의 기능을 활용하여 서로 명확한 관계를 가진 여러 개의 SBOM 파일로부터 하나의 SBOM으로 병합할 수 있습니다.

#### 3.12.1 검증 및 참고 자료

여러 SBOM을 하나로 병합하는 도구가 존재합니다. 예: https://github.com/interlynk-io/sbomasm

#### 3.12.2 배경 및 이유

대규모 소프트웨어 제품의 경우, 전체를 하나의 SBOM으로 제공하는 것보다 각 부분별로 개별 SBOM을 제공하는 것이 더 쉬운 경우가 많습니다.

### 3.13 SBOM Confidentiality
SBOMs MAY be subject to confidentiality agreements. A conformant SBOM MUST NOT, however, be subject to any confidentiality agreements that would prevent a recipient from redistributing the parts of the SBOM applicable to software that such recipient has a right to redistribute.

### 3.13 SBOM 기밀성

SBOM은 기밀유지계약(confidentiality agreement)의 적용을 받을 수 있습니다(MAY).  그러나, 본 가이드에 부합하는 SBOM은 수신자가 재배포 권한이 있는 소프트웨어에 대해 해당 SBOM의 관련 부분을 재배포하는 것을 제한하는 어떠한 기밀유지계약의 적용도 받아서는 안 됩니다(MUST NOT).

#### 3.13.1 검증 및 참고 자료

“NTIA SBOM Minimum elements”, “Access Control” 섹션


#### 3.13.2 배경 및 이유

일부 오픈소스 소프트웨어 라이선스는 수신자가 소프트웨어를 자유롭게 재배포할 수 있도록 허용합니다.  이러한 경우, 수신자 역시 해당 소프트웨어에 적용되는 SBOM의 관련 부분을 재배포할 수 있어야 합니다.

## 4. Conformant notice
소프트웨어에 본 가이드에 부합하는(conformant) SBOM이 포함되어 있음을 표시하고자 할 때, 다음과 같은 안내문을 사용할 수 있습니다(MAY): “This software is supplied with an SBOM conformant to the OpenChain Telco SBOM Guide v1.1, the Guide is available at [https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md)”

Telco Guide 준수 SBOM 내에 다음과 같은 안내문을 선택적으로 사용할 수 있습니다(MAY): “This SBOM conforms to the OpenChain Telco SBOM Guide v1.1 [https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md), it is provided to the recipient free of charge, and the recipient is free to redistribute this SBOM to any third party that they distribute the corresponding software to, provided that they have all the necessary rights to distribute the software to such third party”

소프트웨어 벤더 또는 통신 시스템 공급업체에 RFP, 발주서, 외주 개발 발주 등을 요청할 때, RFP 문서, 발주 문서, 계약 문서 등에서 다음과 같은 안내문을 사용할 수 있습니다(MAY): 
“When releasing software, it is REQUIRED to provide an SBOM compliant with the OpenChain Telco SBOM Guide v1.1 for all software released.  This Guide is available at [https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md)”


## 5. 참고 문헌

* SPDX (ISO/IEC 5962:2021)
  * https://spdx.dev/
  * https://www.iso.org/standard/81870.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081870_ISO_IEC_5962_2021(E).zip
  * SPDX Specification V2.3: https://spdx.github.io/spdx-spec/v2.3/
* OpenChain (ISO/IEC 5230:2020)
  * https://www.openchainproject.org/
  * https://www.iso.org/standard/81039.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081039_ISO_IEC_5230_2020(E).zip
* The Minimum Elements For a Software Bill of Materials (SBOM) a.k.a. “NTIA minimum elements”
  * https://www.ntia.doc.gov/report/2021/minimum-elements-software-bill-materials-sbom
* Framing Software Component Transparency: Establishing a Common Software Bill of Materials (SBOM), Third Edition
  * https://www.cisa.gov/resources-tools/resources/framing-software-component-transparency-2024
* Package URL (PURL)
  * https://github.com/package-url/purl-spec

## 6. 가이드 개정 이력

버전 1.1에서 다음과 같은 업데이트가 이루어졌습니다.

* 패키지 해시로 PackageChecksum과 PackageVerificationCode 모두 허용
* 패키지 해시 항목이 필수(MANDATORY)에서 권장(RECOMMENDED)으로 변경
* ExternalRef 항목이 필수(MANDATORY)에서 권장(RECOMMENDED)으로 변경
* FilesAnalyzed 항목이 더 이상 필수(MANDATORY) 아님
* CISA SBOM Type 예시 추가
* CISA SBOM Type에 대한 권장 문법 추가
* sbomasm을 SBOM 병합 도구의 더 나은 예시로 추가
* 새로운 CISA 문서에 대한 참고 링크 추가

가이드 버전 1.0을 준수하는 SBOM은 버전 1.1도 준수하게 됩니다.  반대로, 버전 1.1을 준수하는 SBOM이 항상 버전 1.0을 준수하는 것은 아닙니다.