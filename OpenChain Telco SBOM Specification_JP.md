# OpenChain 通信業界SBOM仕様 [Draft v 1.0]

## 1. スコープ

本ドキュメント "OpenChain 通信業界SBOM仕様 "は、事業体がソフトウェア部品表（SBOM）をどのように作成し、配信し、そして消費するか、それぞれ関連する要件を概説することを目的とする。本仕様に準拠するSBOMを作成し消費する事業体、または本仕様に準拠するSBOMを作成か消費のどちらかだけを実施する事業体が、SBOMを作成する際と消費する際に、ツールおよびプロセスの再現性と合理性を確保できるようにする。本仕様に適合する事業体がOpenChain Specificationを（どのバージョンでも）採用することを要求するものではないが、本仕様を採用することが大いに推奨されることに留意されたい。

事業体は、SBOMを提供する唯一の方法として本仕様を採用できる。その際、個々のSBOMが本仕様に準拠するのであり、SBOMを提供する事業体ではない。本仕様に準拠したSBOMは「Telco SBOM（通信業界SBOM）」と呼ばれる。

本仕様に準拠したSBOMをリリースすることによって、同じ事業体が同じソフトウェアのSBOMを別の方法や形式で配信することを妨げることはない。ただし、それらのSBOMは本仕様に準拠していないため、事業体もソフトウェア製品も本仕様に準拠しない。

本仕様は、 [Creative Commons Attribution License 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/)の下でライセンスされている。

## 2. 用語と定義

本文書内のキーワード "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY",  "OPTIONAL"は、BCP 14 [[RFC2119]](https://www.ietf.org/rfc/rfc2119.txt) [[RFC8174]](https://www.ietf.org/rfc/rfc8174.txt) に記述されているとおりに解釈される。

### データ形式
データ形式とは、SBOM内の情報のデータ形式を意味する。可能なデータ形式として、SPDX、Cyclone DX、SWID、その他の独自形式、がある。

### 事業体
事業体（entity）とは、第三者（他の組織または個人など）にソフトウェアを頒布する法人（営利、非営利、または（訳注：法人と対比した）個人）を意味する。事業体には、他のグループ会社、または事業体の共通支配下にある会社は含まれない。

### ソフトウェア部品表
ソフトウェア部品表（SBOM）とは、ソフトウェアを構築する際に使用される様々なソフトウェアコンポーネントの詳細とサプライチェーンの関係を含む正式な記録である。

### SBOMタイプ
SBOMは以下のいずれかのタイプである：
* Design,
* Source,
* Build,
* Analyzed,
* Deployed,
* Runtime.

これらタイプの定義については[CISA document](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)を参照すること。


### SPDX
SPDX（Software Package Data Exchange）とは、[ISO標準(ISO/IEC 5962:2021)](https://www.iso.org/standard/81870.html)であり、ソフトウェアパッケージのSBOMを相互に交換するための規格であり、関連するライセンスや著作権情報も含まれる。この標準は[Linux Foundation の SPDXプロジェクト](https://spdx.dev/)によって作成されている。

### OpenChain
OpenChainとは、 [OpenChain ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html)を意味し、オープンソースソフトウェアを組み込んだソフトウェアソリューションを相互に交換する組織間の信頼を構築するベンチマークを提供するために、質の高いオープンソースライセンスコンプライアンスプログラムの主要な要件を規定した国際規格である。 OpenChain Specificationは、Linux Foundationの [OpenChain project](https://www.openchainproject.org)によって作成されている。

### 相互依存関係
相互依存(transitive dependencies)とは、ソフトウェアの実行に必要なすべての ソフトウェアコンポーネントのことである。直接的な依存関係ではないパッケージの依存関係（間接的な依存関係）も含まれる。

### パッケージURL(PURL)
パッケージURL(PURL)とは、ソフトウェアパッケージを一意に識別するためのデファクトスタンダードです。

## 3. 要求要件

### 3.1 データ形式
通信業界SBOM は、ISO/IEC 5962:2021 で標準化されている SPDX データフォーマットのバージョン 2.2 に準拠し、含まれる要素に関して以下に記載する。

#### 3.1.1 検証と参考資料
ISO/IEC 5962:2021 情報技術 - SPDX® 仕様 V2.2.1

#### 3.1.2 根拠
ソフトウェアの供給者と消費者の両方にとって、電気通信サプライチェーンにおけるツールおよび能力の簡素な取り扱いと合理化を確実にするために、通信業界SBOMは、ISO/IEC 5962:2021で標準化されているSPDXデータ形式に準拠しなければならない。 各組織の対外窓口で、本標準SBOMデータ形式を使用することで、ソフトウェアを供給する組織と消費する組織の間の複雑さが簡素化される。

事業体は、内部使用のために代替データ形式を自由に使用することができ、また、SBOMを要求する組織に対して、あるいはソフトウェアの供給者が自発的に、代替データ形式でSBOMを提供することができる。 本OpenChain 通信業界SBOM仕様は準拠すべきSBOM仕様であり、準拠すべき組織の仕様ではない。本OpenChain 通信業界SBOM仕様に適合する事業体は存在せず、OpenChain 通信業界SBOM仕様を実装した事業体によって提供された、本OpenChain 通信業界SBOM仕様に適合するSBOMのみが存在する。

### 3.2 通信業界SBOMに含まれるSPDX要素

以下の要素が必須である。

ドキュメント作成情報（Document creation information）
* SPDXVersion: SPDXの必須項目
* DataLicense: SPDXの必須項目
* SPDXID: SPDXの必須項目
* DocumentName: SPDXの必須項目
* DocumentNamespace: SPDXの必須項目
* Creator: SPDXの必須項目
* Created: SPDXの必須項目
* CreatorComment:  “SBOM Build information” に入力できるようにする

パッケージ情報（Package information）
* PackageName: SPDXの必須項目
* SPDXID: SPDXの必須項目
* PackageVersion: NTIAのSBOM最小要素」によって必要とされる
* PackageSupplier:  NTIAのSBOM最小要素」によって必要とされる
* PackageDownloadLocation: SPDXの必須項目
* FilesAnalyzed
* PackageChecksum:  “NTIA SBOM最小要素” によって推奨される
* PackageLicenseConcluded: SPDXの必須項目
* PackageLicenseDeclared: SPDXの必須項目
* PackageCopyrightText: SPDXの必須項目

パッケージはパッケージURL(PURL)によって識別されるべきである。

SPDX要素間の関係
* Relationship: “NTIA SBOM最小要素” により、少なくとも DESCRIBES と CONTAINS が必要とされる

#### 3.2.1 検証と参考資料
NTIA SBOM最小要素

#### 3.2.2 根拠
通信業界の調和を認識し、また可能であればNTIAの最小要素を超える特別な要件の必要性を認識し、期待されるSBOMの要素について業界の見通しを確実にするため、本「OpenChain 通信業界SBOM仕様」を提案する。

“Component Hash” は推奨されるものの、“NTIA SBOM最小要素” には要求として無い。
SPDX では PackageChecksum に対応する。パッケージを一意に識別するために重要なので必須とする。
なお、ほとんどのSCAツールはハッシュを生成する機能を持っている。

パッケージURL(PURL)は、ソフトウェアパッケージを一意に識別するためのデファクトスタンダードです。

### 3.3 機械が読み取り可能なデータ形式
The Telco SBOM SHALL include, at a minimum, the SPDX in the following machine readable format as default: Tag:Value

#### 3.3.1 検証と参考資料
Tag:Value is described here in SPDX 2.2 https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements

#### 3.3.2 根拠
SBOMには3つの主要フォーマットがある： SPDX、CycloneDX、SWID
これら3つのフォーマットは、NTIAの文書「The Minimum Elements For a Software Bill of Materials (SBOM)」（参考文献のセクションを参照）で推奨されている。

通信業界SBOM仕様のデータ形式としてSPDXを選択した理由は以下の通り:
* SPDXはISO規格であること,
* SPDXはCycloneDXと比較してライセンスコンプライアンスのための機能が充実していること,
* SPDXは人間が読めるフォーマットであること（CycloneDXはJSONとXMLしかない）,
* SWIDは本格的なSBOMフォーマットというよりはソフトウェア識別子である.

簡素化されたツールチェーンを促進するために、本仕様に適合するSBOMは機械可読性が必要がある。また、再現性と整合性を確保するために、本仕様に適合するSBOMは「Tag:Value形式」でなければならない。なお、事業体はその他の機械可読データ形式をリリースすることはできるが本仕様に準拠する必要はない。

「Tag:Value形式」は最も人間が読みやすいフォーマットであり、様々なSPDXフォーマット間のコンバーターが存在する。
(例、https://tools.spdx.org/app/convert/).

### 3.4 人間が読み取り可能なデータ形式
通信業界SBOM は、最低限、デフォルトとして「Tag:Value形式」の人間が読める形式の SPDX を含めるものとする

#### 3.4.1 検証と参考資料
「Tag:Value形式」は SPDX 2.2 を参照（https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements）

#### 3.4.2 根拠
「Tag:Value形式」は人間が読むこともできるため、標準化された機械が読み取り可能なデータ形式と人間が読み取り可能なデータ形式の両方の要件を1つのファイルで満たすことができる。事業体は、さらに人間が読み取り可能なデータ形式をリリースすることができるが、本仕様に準拠する必要はない。

### 3.5 SBOM ビルド情報
本仕様に準拠する SBOM は、いつ作成されたか（SPDX の `Created` フィールドを使用）という情報と、どのバージョンのソフトウェアで作成されたか（SPDX の `CreatorComment` フィールドを使用）という情報を含めなければならない。

SPDX の `Created` フィールド は:
* `Organization`キーワードを示す行を含まなければならない;
* `Tool`キーワードを示す行を記述しなければならない。またこの行では、`Tool`キーワードの後にツール名とツールバージョンを記述しなければならない。

ツール名とツールバージョンはハイフン("-")で区切るべきである。

Telco SBOM仕様に準拠するSBOMは、CreatorCommentフィールドに[CISA](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)が定義するSBOM Typeを提供しなければならない。

#### 3.5.1 検証と参考資料
SPDX規格

#### 3.5.2 根拠
どのツールのどのバージョンでSBOMが作成されたかを知ることは重要である。

SPDX 規格では、例として「toolidentifier-version」を挙げているが、この構文が必須というわけではない。

例えば、出力するツールを示す際に：
```
Creator: Tool: sigs.k8s.io/bom/pkg/spdx
```
他の例として:
```
Creator: Tool: scancode-toolkit 30.1.0
```
別の例として、
```
Creator: Tool: SCANOSS-PY: 1.5.1
```
ここで、名前にはハイフンが含まれ、ツール名とツールバージョンはハイフンで区切られていない。

従って、正確な構文を要求することはできない。

### 3.6 SBOM納入のタイミング
SBOM は、遅くともソフトウェア（バイナリ形式またはソース形式のいずれか）の引渡しの時点までに納品しなければならない。

#### 3.6.1 検証と参考資料
NTIA SBOM最小要素 の “Distribution and Delivery”セクション

#### 3.6.2 根拠
納品される側の事業体がソフトウェアとそのSBOMを確実に受け取ることができるように、SBOMはソフトウェアの納品よりも遅くならないように引渡さなければならない。ソフトウェアの発注者が指示した場合は、ソフトウェアの引き渡し前にSBOMが納品されてもよいが、本仕様への準拠を確実にするためにソフトウェアの納品時には対応するSBOMも納品をしなければならない。

### 3.7 SBOMの納入方法
技術的に可能な場合、SBOM はソフトウェア「パッケージ」に埋め込まなければならない。スペースに制約のある組込みシステムの場合など、提供されるソフトウェア「パッケージ」に SBOM を組み込むことが技術的に不可能な場合、ソフトウェア供給側（受注者側）は少なくとも 18ヶ月利用可能な SBOM のウェブホスト版を提供し、ソフトウェア受信側（発注者）が自身の使用のためにこれらをローカルにコピーし保存する能力をいかなる形でも制限してはならない。このような制限は、追加の秘密保持契約において受領者に課してはならない。

#### 3.7.1 検証と参考資料
NTIA SBOM最小要素 の “Distribution and Delivery”セクション

#### 3.7.2 根拠
ウェブホスティングなどでSBOM を提供する手法は安定性が低く、またアクセスが長期間保証されない。このように、SBOM をソフトウェアの「パッケージ」に含めることが技術的に不可能なシナリオでは、SBOM をオンラインで公開することが許可される。この期間は、再認証に関する "OpenChain specification" の要求に沿ったものである。

### 3.8 SBOMの範囲
SBOM には、すべての依存関係を含め、製品と共に提供されるすべてのオープンソースソフトウェアを含めるものとする。SBOM には、すべての商用コンポーネントを含めるべきである。

含まれない成分がある場合は、"known unknown "として報告しなければならない。

#### 3.8.1 検証と参考資料
NTIA SBOM最小要素 の “Known Unknowns”セクション

#### 3.8.2 根拠
SBOM に市販のコンポーネント情報を持たせることは、可能、望ましい、実行可能でない、かもしれない。しかしながら、SBOMは可能な限り完全であることが望ましい。

### 3.9 SaaS展開におけるSBOM
本仕様はSBOMレベルでのみ適用されるため、提供するソフトウェアの一部またはすべてに通信業界SBOMを提供することを選択した事業体にとって、SaaS提供物にも通信業界SBOMを提供する要件はない。しかし、事業体は本仕様をSaaS提供物にも適用し、SaaS提供物で使用されるオープンソースソフトウェアとその相互依存関係をSBOMとして提供することができる。

#### 3.9.1 検証と参考資料

#### 3.9.2 根拠
現在のところ、SaaS SBOMが何を含むべきかについて、業界のコンセンサスは得られていない。

### 3.10  コンテナ用SBOM
コンテナ用のSBOMには、コンテナで提供されるすべてのオープンソースコンポーネントを含めるべきである。コンテナにインストールされたパッケージ、コンテナにコピーまたはダウンロードされたコンポーネント、およびコンテナ内でコンパイルされたコンポーネントを構築するために使用された依存関係が含まれる。

#### 3.10.1 検証と参考資料

#### 3.10.2 根拠
提供されるすべてのオープンソースコンポーネントは、SBOMの一部であるべき。

### 3.11 SBOMの検証
SBOM の完全性を保証するために、SBOM のデジタル署名を提供することが推奨される。

#### 3.11.1 検証と参考資料
Sigstore（https://www.sigstore.dev/）は SBOM のデジタル署名の一例である.

#### 3.11.2 根拠
SBOMの検証は重要なトピックであるが、OpenChain Telco-WG は、この作業を当面は他の取り組みに委ね、この文書の将来の改訂でこのトピックを再検討するつもりである。

### 3.12 SBOMのマージ
本仕様に従ったSBOMは、SPDXの関係定義機能を使用して、互いに明確に定義された関係を持った複数のSBOMファイルから構築することができる。

#### 3.12.1 検証と参考資料
複数のSBOMから１つのSBOMへマージするツールの一例： https://github.com/vmware-samples/sbom-composer

#### 3.12.2 根拠
大規模なソフトウェア製品を扱う場合、単一のSBOMよりも、個々の部品のSBOMを提供する方が容易なことが多い。

### 3.13 SBOMの守秘義務
SBOMは秘密保持契約の対象であってもよい。ただし、本仕様に適合するSBOMは、受信者が再配布する権利を持つソフトウェアに適用されるSBOMに対して、受信者の再配布を妨げるような秘密保持契約の対象になってはならない。

#### 3.13.1 検証と参考資料
NTIA SBOM最小要素 の “Access Control”セクション

#### 3.13.2 根拠
オープンソースソフトウェアライセンスの中には、いかなる受領者もソフトウェアを再配布できるものがある。このような状況では、受信者もSBOMの関連部分を再配布できるようにすべきである。

## 4. 適合通知
ソフトウェアがSBOMに適合していることを示すために、以下の記述を使用してもよい： "このソフトウェアは、OpenChain Telco SBOM Specification v1.0に準拠したSBOMとともに提供される。この仕様は、https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md で入手できる。"

このSBOMはOpenChain Telco SBOM仕様v1.0  https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md に準拠しており、受領者には無償で提供される。受領者は、対応するソフトウェアを配布するいかなる第三者に対しても、当該第三者にソフトウェアを配布するために必要なすべての権利を有することを条件に、このSBOMを自由に再配布することができる。

ソフトウェアベンダーや通信システムサプライヤーにRFP、購買発注、受託開発発注を依頼する場合、RFP文書、発注文書、契約文書の記載事項として、以下の文を使用してもよい。
ソフトウェアをリリースする場合、リリースされるすべてのソフトウェアについて、OpenChain Telco SBOM Specification v1.0に準拠したSBOMを提供することが要求される。 この仕様は"[https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain%20Telco%20SBOM%20Specification.md) "で入手可能である。

## 5. 参考文献

* SPDX (ISO/IEC 5962:2021)
  * https://spdx.dev/
  * https://www.iso.org/standard/81870.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081870_ISO_IEC_5962_2021(E).zip
* OpenChain (ISO/IEC 5230:2020)
  * https://www.openchainproject.org/
  * https://www.iso.org/standard/81039.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081039_ISO_IEC_5230_2020(E).zip
* The Minimum Elements For a Software Bill of Materials (SBOM) （本資料内で "NTIA SBOM最小要素" と記載）
  * https://www.ntia.doc.gov/report/2021/minimum-elements-software-bill-materials-sbom
* Package URL (PURL)
  * https://github.com/package-url/purl-spec

