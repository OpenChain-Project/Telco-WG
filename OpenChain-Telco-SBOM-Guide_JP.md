# OpenChain Telco SBOM Guide Version 1.1

本書は英文を翻訳したものです。この翻訳と英文との間に何らかの相違がある場合は英文が優先されるものとします。

## 1. スコープ

本文書 "OpenChain Telco SBOM Guide" は、エンティティがソフトウェア部品表（SBOM：Software Bill of Materials）を作成・提供・利用する方法に関連する特定の要件を概説することを目的とし、本ガイドに準拠するSBOMを作成および/または利用するエンティティが、SBOMを作成および利用するためのツールおよびプロセスの再現性と合理性を確保できるようにします。

本ガイドは、本ガイドに適合するエンティティに対して、OpenChain （OpenChain Specificationのどのバージョンでも）を採用することを要求するものではありませんが、OpenChainを採用することが大いに推奨されることに留意ください。

このガイドはSBOM単位で適応できるように設計されており、エンティティはSBOMを提供する唯一の方法として本ガイドを使用できるものの、本ガイドが参照するのは個々のSBOMであり、SBOMを提供するエンティティではありません。
本ガイドに沿ったSBOMを「OpenChain Telco SBOM Guide Compatible」と呼ぶことができます。

本ガイドの要件に一致するSBOMをリリースすることは、同じソフトウェアのSBOMを別の方法または形式で配信することを妨げるものではありません。

本ガイドは [Creative Commons Attribution License 4.0 (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/)の下にライセンスされています。


## 2. 用語と定義

本文書に記載の、 "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY",  "OPTIONAL"は、BCP 14 [[RFC2119]](https://www.ietf.org/rfc/rfc2119.txt) [[RFC8174]](https://www.ietf.org/rfc/rfc8174.txt) の記述とおりに解釈されます。

### データフォーマット
データフォーマット（Data Format）とは、SBOM内の情報のデータフォーマットを意味します。可能なデータフォーマットとして、SPDX、Cyclone DX、SWID、その他の独自フォーマット、があります。

### エンティティ
エンティティ（entity）とは、第三者（他の組織または個人など）に対して、ソフトウェアを頒布する法人（営利・非営利は問わない）、または 個人を意味します。エンティティには、グループ会社、エンティティの共通支配下にある会社、は含まれません。

### ソフトウェア部品表
ソフトウェア部品表（SBOM）とは、ソフトウェアを構築する際に使用される様々なソフトウェアコンポーネントの詳細とサプライチェーンの関係を含む正式な記録です。

### SBOMタイプ
SBOMは以下のいずれかのタイプがあります：
* Design,
* Source,
* Build,
* Analyzed,
* Deployed,
* Runtime.

これらタイプの定義については[CISA document](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)を参照ください。


### SPDX
SPDX（Software Package Data Exchange）とは、[ISO標準(ISO/IEC 5962:2021)](https://www.iso.org/standard/81870.html)であり、ソフトウェアパッケージのSBOMを相互に交換するための規格であり、関連するライセンスや著作権情報も含まれます。この標準は[Linux Foundation  SPDXプロジェクト](https://spdx.dev/)によって作成されています。

### OpenChain
OpenChainとは、 [OpenChain Specification ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html)を意味し、オープンソースソフトウェアを組み込んだソフトウェアソリューションを相互に交換する組織間の信頼を構築するベンチマークを提供するために、質の高いオープンソースライセンスコンプライアンスプログラムの主要な要件を規定したISO/IEC国際規格です。 "OpenChain Specification" は、Linux Foundation配下の [OpenChain project](https://www.openchainproject.org)によって作成されています。

### 推移的依存性
推移的依存性(transitive dependencies)とは、ソフトウェアの実行に必要なすべての ソフトウェアコンポーネントのことです。直接的な依存関係ではないパッケージの依存関係（間接的な依存関係：依存先のOSSがさらに依存するOSSなど）も含まれます。

### パッケージURL（PURL）
パッケージURL（PURL）とは、ソフトウェアパッケージを一意に識別するためのデファクトスタンダードです。

## 3. 要求要件

### 3.1 データフォーマット
本文書 "OpenChain Telco SBOM Guide" と互換性のあるSBOMは、ISO/IEC 5962:2021 で標準化されている SPDX データフォーマットのバージョン 2.2、またはバージョン2.3 に準拠します。含まれる要素に関しては本ガイドの3.2節に記載します。

#### 3.1.1 検証と参考資料
* ISO/IEC 5962:2021 Information technology - SPDX® Specification V2.2.1
* [SPDX® Specification V2.3](https://spdx.github.io/spdx-spec/v2.3/)

#### 3.1.2 根拠
ソフトウェアの提供者および利用者の双方にとって、通信業界のサプライチェーンにおけるツールや能力の簡略化と効率化を実現するため、本文書 "OpenChain Telco SBOM Guide" はISO/IEC 5962:2021で標準化されているSPDXデータフォーマットに準拠する必要があります。 本SBOMデータフォーマットを採用することにより、統一された要求事項が1セットのみ適用されるため、ソフトウェアを供給する組織と利用する組織の双方にとって複雑さが簡素化されます。

エンティティは、エンティティ内部での使用のために代替データフォーマットを自由に使用することができます。また、SBOMを要求（利用）する組織に対して、あるいはソフトウェアの供給者が自発的に代替データフォーマットでSBOMを提供することができます。 本文書 "OpenChain Telco SBOM Guide" は、SBOMレベルの仕様であり、組織レベルの仕様ではありません。このガイドに準拠するのは、組織ではなくSBOMそのものであり、"OpenChain Telco SBOM Guide" を実装した組織によって提供されるSBOMが該当します。


### 3.2 OpenChain Telco SBOM Guideに互換性のあるSBOMに含まれるSPDX要素

以下が必須要素です。

Document creation information:
* SPDXVersion:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* DataLicense:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* SPDXID:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* DocumentName:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* DocumentNamespace:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* Creator:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* Created:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* CreatorComment:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“SBOM Build information” に入力できる


Package information:
* PackageName:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* SPDXID:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* PackageVersion:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“NTIA SBOM Minimum elements” によって必要とされる項目
* PackageSupplier:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“NTIA SBOM Minimum elements” によって必要とされる項目
* PackageDownloadLocation:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDXの必須項目
* PackageLicenseConcluded:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDX2.2の必須項目
* PackageLicenseDeclared:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDX2.2の必須項目
* PackageCopyrightText:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SPDX2.2の必須項目

PackageChecksumまたはPackageVerificationCodeの2つのうち1つが推奨：  “NTIA SBOM Minimum elements” によって推奨される項目

パッケージは、 Package URL(PURL) によって識別されるべきです。

PURLが存在する場合、ExternalRefフィールドに入れるべきです。例えば：
```
ExternalRef: PACKAGE-MANAGER purl pkg:pypi/django@1.11.1
```

SPDX要素間の関係
* Relationship: “NTIA SBOM Minimum elements” により、少なくとも DESCRIBES と CONTAINS が必要とされる項目

#### 3.2.1 検証と参考資料
NTIA SBOM Minimum elements

#### 3.2.2 根拠
Telco業界の調和と特別な要求事項の必要性を認識し、期待されるSBOMの要素について業界の予測可能性を確保するために、本文書 "OpenChain Telco SBOM Guide" を提案します。

“Component Hash” は推奨されるものの、“NTIA SBOM Minimum elements” には要求されていません。

SPDX では、PackageChecksum または PackageVerificationCode に対応します。
なお、ほとんどのSCA（Software Composition Analysis）ツールはハッシュを生成する機能を持っています。

CISA文書 ["Framing Software Component Transparency: Establishing a Common Software Bill of Materials (SBOM), Third Edition"](https://www.cisa.gov/resources-tools/resources/framing-software-component-transparency-2024) の2.5節の "Table 1" を参照ください。

パッケージURL（PURL）は、ソフトウェアパッケージを一意に識別するためのデファクトスタンダードです。

### 3.3 機械が読み取り可能なデータフォーマット
本文書 "OpenChain Telco SBOM Guide" に互換性のあるSBOMは、機械が読み取り可能なデータフォーマットである「Tag:Value形式」または「JSON形式」のどちらかの形式とします。

#### 3.3.1 検証と参考資料
「Tag:Value形式」と「JSON形式」は以下を参照ください。

* SPDX 2.2： https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements
* SPDX 2.3： https://spdx.github.io/spdx-spec/v2.3/conformance/#44-standard-data-format-requirements

#### 3.3.2 根拠
SBOMには3つの主要フォーマットがあります： SPDX、CycloneDX、SWID

これら3つのフォーマットは、NTIAの文書「The Minimum Elements For a Software Bill of Materials (SBOM)」（参考文献のセクションを参照）で推奨されています。

 "OpenChain Telco SBOM Guide" に互換性のあるSBOMのデータフォーマットとしてSPDXを選択した理由は以下の通りです:
* SPDXは、ISO規格であるため
* SPDXは、CycloneDXと比較してライセンスコンプライアンスのための機能が充実しているため
* SPDXは、人間が読めるフォーマットであるため（CycloneDXはJSONとXMLしかない）
* SWIDは、本格的なSBOMフォーマットというよりはソフトウェア識別子であるため

簡素化されたツールチェーンを促進するために、本ガイドに適合するSBOMは機械が読み取り可能なデータフォーマットである必要があります。また、再現性と整合性を確保するために、本ガイドに適合するSBOMは「Tag:Value形式」または「JSON形式」でなければなりません。なお、エンティティは、その他の機械が読み取り可能なデータフォーマットをリリースすることができるものの、本ガイドに準拠する必要はありません。

「Tag:Value形式」は最も人間が読みやすい形式であり、様々なSPDXフォーマット間のコンバーターが存在します(例えば、https://tools.spdx.org/app/convert/)。
また、「JSON形式」はいくつかのツールによって提供される形式です。

### 3.4 人間が読み取り可能なデータフォーマット
本文書 "OpenChain Telco SBOM Guide" に互換性のあるSBOMは、人間が読み取り可能なデータフォーマットである「Tag:Value形式」または「JSON形式」のどちらかの形式とします。

#### 3.4.1 検証と参考資料
「Tag:Value形式」と「JSON形式」は SPDX 2.2 を参照ください。
（https://spdx.github.io/spdx-spec/v2.2.2/conformance/#44-standard-data-format-requirements）

#### 3.4.2 根拠
「Tag:Value形式」は人間が読むこともできるため、標準化された "機械が読み取り可能なデータフォーマット" と "人間が読み取り可能なデータフォーマット" の両方の要件を1つのファイルで満たすことができます。なお、エンティティは、その他の人間が読み取り可能なデータフォーマットをリリースすることができるが、本ガイドに準拠する必要はありません。

### 3.5 SBOM ビルド情報
本文書 "OpenChain Telco SBOM Guide" に互換性のあるSBOM は、いつ作成されたか（SPDX の `Created field` を使用）という情報と、どのバージョンのソフトウェアで作成されたか（SPDX の `CreatorComment field` を使用）という情報を含めなければならなりません。

SPDX の `Created field` とは:
* `Organization`キーワードを示す行を含まなければなりません。
* `Tool`キーワードを示す行を記述しなければなりません。かつ、この行では `Tool`キーワードの後にツール名とツールバージョンを記述しなければなりません

また、ツール名とツールバージョンはハイフン("-")で区切るべきです。

本文書 "OpenChain Telco SBOM Guide" に互換性のあるSBOM は、`CreatorComment field`に[CISA](https://www.cisa.gov/sites/default/files/2023-04/sbom-types-document-508c.pdf)が定義するSBOM Typeの情報を提供しなければなりません。

SBOM Typeを示す推奨構文は、"SBOM Type: xxx" です。 “xxx” は、 “Design”, “Source”, “Build”, “Analyzed”, “Deployed”, “Runtime” の６つのうちのいずれかです。

#### 3.5.1 検証と参考資料
SPDX規格

#### 3.5.2 根拠
どのツールのどのバージョンでSBOMが生成されたかを知ることは重要です。

SPDX 規格では、例として「Tool: toolidentifier-version」という記述例を挙げているが、この構文が必須というわけではありません。

例えば、出力するツールを示す際に：
```
Creator: Tool: sigs.k8s.io/bom/pkg/spdx
```
他の例として:
```
Creator: Tool: scancode-toolkit 32.3.0
```
また別の例として：
```
Creator: Tool: SCANOSS-PY: 1.18.1
```
上の例では、名前にはハイフンが含まれ、ツール名とツールバージョンはハイフンで区切られていません。

従って、正確な構文（SPDXに規定される "Tool: toolidentifier-version" のように、ツールとバージョンの間をハイフンで結ぶ構文）を要求することはできません。

`CreatorComment field`はフリー・テキスト・フィールドです。SPDX 2.2および2.3にはCISA SBOM Type用の特定のフィールドがないため、CISA SBOM Typeを格納するためにこのフィールドを使用するが、もちろん他の情報も格納できます。

本文書 "OpenChain Telco SBOM Guide" では、特定のフォーマットを要求しません。
どのような場合でも、「Design」、「Source」、「Build」、「Analyzed」、「Deployed」、「Runtime 」のうち、少なくとも1つの単語が存在すればよいです。

したがって、以下の構文はすべて有効です。なお、１つ目の例が推奨されます：

```
CreatorComment: SBOM Type: Deployed
```
```
CreatorComment: Analyzed
```
```
CreatorComment: This SBOM was created during build phase.
```

### 3.6 SBOM納入のタイミング
SBOM は、遅くともソフトウェア（バイナリ形式またはソース形式のいずれか）の引渡しの時点までに納品しなければならなりません。

#### 3.6.1 検証と参考資料
"NTIA SBOM Minimum elements" の “Distribution and Delivery” セクション

#### 3.6.2 根拠
納品されるエンティティが、納品されるソフトウェアとSBOMの両方を確実に受け取ることができるように、SBOMはソフトウェアの納品よりも遅くならないように納品さなければならなりません。
ソフトウェアの発注者が指示した場合は、ソフトウェアの納品前にSBOMが納品されてもよいが、本ガイドへの準拠を確実にするために、ソフトウェアの納品時にはSBOMも納品をしなければなりません。

### 3.7 SBOMの納入方法
技術的に可能な場合、SBOM はソフトウェア「パッケージ」に埋め込まなければなりません。スペースに制約のある組込みシステムの場合など、提供されるソフトウェア「パッケージ」に SBOM を組み込むことが技術的に不可能な場合、ソフトウェア供給者（受注者）は少なくとも 18ヶ月間利用可能な SBOM のウェブホスト版を提供し、ソフトウェア受領者（発注者）が自身の使用のためにこれらをローカルにコピーし保存する能力をいかなる形でも制限してはなりません。このような制限は、秘密保持契約の追加項目においてもソフトウェア受領者に課してはなりません。

#### 3.7.1 検証と参考資料
"NTIA SBOM Minimum elements" の “Distribution and Delivery” セクション

#### 3.7.2 根拠
ウェブホスティングなどでSBOM を提供する手法は安定性が低く、またアクセスが長期間保証されません。このように、SBOM をソフトウェアの「パッケージ」に含めることが技術的に不可能なシナリオでは、SBOM をオンラインで公開することが許可されます。この公開期間（18ヶ月）は、再認証に関する [OpenChain Specification ISO/IEC 5230:2020](https://www.iso.org/standard/81039.html) の要求に沿ったものです。

### 3.8 SBOMの範囲
SBOM には、すべての依存関係を含め、製品と共に提供されるすべてのオープンソースソフトウェアを含めるものとします。SBOM には全ての商用コンポーネントを含めるべきです。

含まれない成分がある場合は、"known unknowns" として報告しなければなりません。

#### 3.8.1 検証と参考資料
"NTIA SBOM Minimum elements" の “Known Unknowns” セクション

#### 3.8.2 根拠
SBOMに商業的なコンポーネント情報を含めることは、可能でない場合や推奨されない場合、または現実的でない場合があります。しかしながら、SBOMは可能な限り完全であることが推奨されます。

### 3.9 SaaSで提供されるサービスのSBOM
本文書 "OpenChain Telco SBOM Guide" は、SBOMレベルでのみ適用されるため、あるエンティティがそのソフトウェア提供にこのガイドを採用したとしても、SaaSサービスについても同じ対応をしなければならないという義務はありません。
しかし、エンティティが希望すれば、 "OpenChain Telco SBOM Guide" をSaaS提供物にも適用して、そのSaaSで使用されているオープンソースソフトウェアや依存関係を含むSBOMを提供することができます。


#### 3.9.1 検証と参考資料

#### 3.9.2 根拠
現在、業界ではSaaSのSBOMに何を含めるべきかについての統一された意見はありません。

### 3.10  コンテナ用SBOM
コンテナ用のSBOMには、コンテナで提供されるすべてのオープンソースコンポーネントを含めるべきでです。
これには、コンテナにインストールされたパッケージ、コンテナにコピーまたはダウンロードされたコンポーネント、またコンテナ内でコンパイル済のコンポーネントを構築するために使用された依存関係のあるコンポーネント、が含まれます。

#### 3.10.1 検証と参考資料

#### 3.10.2 根拠
提供されるすべてのオープンソースコンポーネントは、SBOMの一部として含まれるべきです。

### 3.11 SBOMの検証
SBOM の完全性（integrity）を保証するために、SBOM のデジタル署名を提供することが推奨されます。

#### 3.11.1 検証と参考資料
Sigstore (https://www.sigstore.dev/) は SBOM のデジタル署名の１つの例です。

#### 3.11.2 根拠
SBOMの検証は重要なトピックですが、OpenChain Telco Working Group は、この作業を当面は他の取り組みに委ね、この文書の将来の改訂でこのトピックを再検討します。

### 3.12 SBOMのマージ
本ガイドに従ったSBOMは、SPDXの関係定義機能を使用して、それぞれが明確な関係を持つ複数のSBOMファイルから構築することができます。

#### 3.12.1 検証と参考資料
複数のSBOMから１つのSBOMへマージするツールの１つの例： [https://github.com/opensbom-generator/sbom-composer](https://github.com/interlynk-io/sbomasm)

#### 3.12.2 根拠
大規模なソフトウェア製品を扱う場合、単一のSBOMよりも、個々の部品のSBOMを提供する方が容易なことが多いです。

### 3.13 SBOMの守秘義務
SBOMは機密保持契約の対象となる場合があります。ただし、本ガイドに適合するSBOMは、SBOMを受け取った人が再配布する権利のある部分について、その再配布を妨げるような機密保持契約であってはなりません。

#### 3.13.1 検証と参考資料
"NTIA SBOM Minimum elements" の “Access Control”セクション

#### 3.13.2 根拠
オープンソースソフトウェアライセンスの中には、いかなる受領者もソフトウェアを再頒布できるものがあります。このような状況では、受領者もSBOMの関連部分を再頒布できるようにすべきです。

## 4. 適合通知
ソフトウェアがSBOMに適合していることを示すために、以下の記述を使用してもよい：

"このソフトウェアは、"OpenChain Telco SBOM Guide v1.1" に準拠したSBOMとともに提供されます。このガイドは、[https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md)で入手できます。"

"このSBOMは "OpenChain Telco SBOM Guide v1.1（[https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md)）" に準拠しており、受領者には無償で提供されます。受領者は、対応するソフトウェアを頒布するいかなる第三者に対しても、当該第三者にソフトウェアを頒布するために必要なすべての権利を有することを条件に、このSBOMを自由に再頒布することができます。"

また、ソフトウェアベンダーや通信システムサプライヤーにRFP、購買発注、受託開発発注を依頼する場合、RFP文書、発注文書、契約文書の記載事項として、以下の文を使用してもよい：

"ソフトウェアをリリースする場合、リリースされるすべてのソフトウェアについて、"OpenChain Telco SBOM Guide v1.1" に準拠したSBOMを提供することを要求します。 このガイドは"[https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md](https://github.com/OpenChain-Project/Telco-WG/blob/main/OpenChain-Telco-SBOM-Guide_EN.md)"で入手できます。"

## 5. 参考文献

* SPDX (ISO/IEC 5962:2021)
  * https://spdx.dev/
  * https://www.iso.org/standard/81870.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081870_ISO_IEC_5962_2021(E).zip
  * SPDX Specification V2.3: https://spdx.github.io/spdx-spec/v2.3/
* OpenChain (ISO/IEC 5230:2020)
  * https://www.openchainproject.org/
  * https://www.iso.org/standard/81039.html
  * https://standards.iso.org/ittf/PubliclyAvailableStandards/c081039_ISO_IEC_5230_2020(E).zip
* The Minimum Elements For a Software Bill of Materials (SBOM) （本資料内で "NTIA SBOM Minimum elements" と記載）
  * https://www.ntia.doc.gov/report/2021/minimum-elements-software-bill-materials-sbom
* Framing Software Component Transparency: Establishing a Common Software Bill of Materials (SBOM), Third Edition
  * https://www.cisa.gov/resources-tools/resources/framing-software-component-transparency-2024
* Package URL (PURL)
  * https://github.com/package-url/purl-spec
 

## 6. 変更履歴
"OpenChain Telco SBOM Guide" のバージョン1.1で以下の更新が行われました。

* "package hash" として "PackageChecksum" と "PackageVerificationCode" の両方を使用可能に
* "The package hash" を "MANDATORY"　から "RECOMMENDED" へ変更
* "ExternalRef" を "MANDATORY" から "RECOMMENDED" へ変更
* "FilesAnalyzed" を "MANDATORY" から外した
* "CISA SBOM Types" の例を追記
* "CISA SBOM Types" の記述構文を追記
* "SBOM merge tool" の例を "sbomasm" へ変更
* CISA document（Framing Software Component Transparency）を参考文献に新規追加

"OpenChain Telco SBOM Guide" のバージョン1.0に準拠したSBOMは、バージョン1.1にも準拠します。
ただし、その逆は当てはまりません。

