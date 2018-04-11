# アノテーション仕様書

Reference from [SemEval-2016 Task 5](http://alt.qcri.org/semeval2016/task5/data/uploads/absa2016_annotationguidelines.pdf)

## アノテーションの概要

有価証券報告書について、極性(Sentiment)、およびその対象(Target)と観点(Aspect)をアノテーションすることが目的となる。

例: 株式会社ガンバルの売り上げは、好調だった。

* Target: 株式会社ガンバル
* Aspect: Entity=`company`、Attribute=`sales`
* Sentiment: `positive`

Aspectは、EntityとAttributeのセットで定義される。上記の場合、Entity=`company`、Attribute=`sales`となる。EntityとAttributeは、事前に定義されたいくつかの種類の中から選択式で設定される。例えば、Entityは`company`や`product`、Attributeは`sales`や`profit`などのカテゴリから設定される。このE#Aペアが「観点」となる。

Targetは、Entityの具体的な記述となる(E#Aペアの**E**に相当)。

各E#Aペアは、極性を持つ。極性は(`positive`,`negative`,`neutral`)の中から設定される。Sentimentが読み取れるがpositiveともnegativeともはっきり言えない場合`neutral`を付与する。

* 本社の業績は好調であった: `positive`
* 本社の業績は下降気味であった: `negative`
* 本社の業績は前年並みであった、不透明である: `neutral`
* 本社の売上は100億円だった: {}  # どんな極性もよみとれない

このアノテーションは文単位で行われるもので、他の文のEntityを参照したり、他の文のSentimentの考慮といったことは行わない。あくまで、提示された一文内でE#Aペア、極性を判断することとする(SemEval2016では周辺の文を考慮しているが、レビューなどに比べ有価証券報告書は長すぎるため、各文は独立して評価を行う)。

## アノテーション要素の定義

### Targetの定義

Targetとして指定するのは、固有表現、もしくは固有表現と認識されうる名詞/名詞の連続を対象とする(=「の」などで連携されるものは対象とならない)。

* インドでの販売が、下半期に入り高額紙幣切り替えの影響で一時的に減少しました
  * Entity「販売」が「減少」(「インドでの販売」ではない)
* 国内、中国、EMEAの中小型の減・変速機の市況
  * 「市況」がEntity

### Aspectの定義

Entity、およびAttributeの種類は以下とする。

**Entity**

* market: 生鮮食品市場・原油市況といった、市場、市況を表す語
* company: 会社/法人、グループを表す語
* business: 機械部品部門・国内事業など、会社内の部門、事業部、事業領域を表す語
* product: エンジン・バイク、工場建設・プリントサービスといった、製品、またサービスの名称を表す語

**Attribute**

* sales: 売上を表す語
* profit: 利益を表す語
* amount: 販売数量、生産数量などを表す語
  * 企業がアウトプットする量。つまり、需要はこれに当たらない。ただ、生産量とほぼ同じ意味で使われることがあるので、これは文脈から判断する。
* price: 野菜価格、製品価格といった販売単価を表す語
  * 販売価格についての言及に付与する。「原料価格」はcostとして扱う
* cost: 売上原価、労務費といった原価を表す語

### Sentimentの定義

結果のみを対象にする

* x: 国内事業の売り上げ増加に取り組みました=>取り組んだだけで、結果どうなったかはわからない
  * 実現していない活動: 強化します、改善に取り組みましたetc
  * 実現していない未来、予測: 上向く予定です、改善「傾向」にあります、下振れさせるリスク、懸念etc
* o: 国内事業の売上は増加しました

それ自体が極性を持たないものは対象としない。

* x: 社会構造の変化、金融資本市場の変動、消費者の皆様の生活防衛意識の高まりや節約志向
  * これらは、それ自体はpositiveでもnegativeでもない

極性の判定は、文単位で行う。前後の文脈からpositiveだと推定できても、その文ではnegativeならnegativeとする。

### Examples

**market**

*また、**宝飾市況**においては、インバウンド需要の減速及び個人消費の本格的な回復が見込めず、依然厳しい環境の下推移いたしました*

* 宝飾市況: `market#general, negative`

**company**

*また、営業外における**中国合弁会社**の業績回復に伴う持分法による投資利益の改善がグループ収益に寄与いたしました *

* 中国合弁会社: `company#general, positive`

**business**

*当連結会計年度の業績につきましては、**ビッグデータ関連事業**、**サービス企画開発事業**ともに受注件数が増加しておりますが、特にビッグデータ関連事業が業績を牽引いたしました*

* ビッグデータ関連事業: `business#amount, positive`
* サービス企画開発事業: `business#amount, positive`

*なお、**ゲーム事業**の原価が主に人件費等であり売上高の減少に関わらず一定額を要することから、上記未受注による売上高の減少の影響により、想定を大きく上回る未配属原価を計上することとなりました*

* ゲーム事業: `business#cost, neutral`

**product**

*なお、当連結会計年度の生産量は、ブナピーを含め**ブナシメジ**42,602ｔ（同5.5％増）、**エリンギ**19,250ｔ（同0.2％減）、**マイタケ**14,281ｔ（同4.3％増）となりました*

* ブナシメジ: `product#amount, positive`
* エリンギ: `product#amount, positive`
* マイタケ: `product#amount, positive`

### E#Aのいずれかの欠損について

positive/negativeの判定が可能だが、Entity/Attributeが特定できない場合は以下の基準に準ずる。

|               | Attribute: あり      | Attribute: 対象外    |
|---------------|----------------------|----------------------|
| Entity: あり  | (通常)               | (Entityタグ)#general |
| Entity:なし   | NULL#(Attributeタグ) | NULL#general         |
| Entity:対象外 | OOD#general          | OOD#general          |

* Entityなし、Attributeあり => Entityに`NULL`を指定し、TargetはAttributeを選択する
  * 例: 「売上高は15%増加しました」 `sales`の判定が可能だが、Entityがない
  * `NULL#sales`となり、*Targetは`売上高`を選択する*
* Entityあり、Attributeなし=Attributeが対象外
  * positive/negativeの判定ができるということはAttributeがないわけではなく対象外、というケースになる。
  * 例: 「音楽事業部は好調だ」 `business`のEntityがあるが、該当するAttributeがない
  * この場合、Attributeに`general`を使用し`business#general, positive`とする
* Entityなし、Attributeなし(=対象外)
  * Entityがなく、対象外のAttributeのみある場合はアノテーションを行なっていない
  * 例: 「このような取り組みの結果、好調な結果となった」
  * この場合、Entityに`NULL`、Attributeに`general`を選択し、TargetはAttributeの表現を選択する
  * `NULL#general`、*Target=`好調`*。対象表現は、形態素解析の結果に基づき該当の一要素を指定する。
* Entityなし(=対象外)、Attributeあり/Attributeなし(=対象外)
  * Entityが何らかの形で特定できる場合は`OOD`(Out of Domain)を指定する。
  * OODの場合、Attributeの有無にかかわらず`general`でpositive/negativeのみアノテートする

一文に、同じEntityに対し複数のAttributeが登場する場合は同じTargetに対し複数回アノテーションを行う。

* 株式会社ガンバルの売り上げ、利益はともに向上した
  * 株式会社ガンバル/売り上げ/向上した: `company#sales, positive`
  * 株式会社ガンバル/利益/向上した: `company#profit, positive`

## アノテーションガイド

1. 一文の中で極性が現れている箇所を特定する。
   * 極性の表現が対象のAttributeでない場合、Attributeは`general`とする
2. 主語がない場合、Entityは`NULL`としTargetとしてAttributeに関する記述(売上、利益etc)を指定する
3. 主語があるがアノテーション対象でない場合、Entityは`OOD`としAttributeは`general`で極性のみアノテーションする 
4. 主語がある場合、その主語を`Target`とする。
   * 直接の主語をとるよう注意する: *「調理冷凍食品事業ではエビ加工品やかに風味かまぼこの販売が伸長しました」では、販売が伸長したのはエビ&カニ風味で、事業でない*
   * 固有表現と認識される名詞/連続した名詞を対象とする: *`二輪車向けエンジン`など、途中で接尾辞(向け)が入っているケースがあるので、注意する。この場合は、`エンジン`が対象になる*。ただ、事業部名や特定製品名など、会社の中でそれを一語の固有表現として扱っている場合はそれを優先する
   * 「国内事業部収入」や「音楽製品売上」といった、EntityとAttributeが結合したような語は、「国内事業部収入」(Entityなし、Attribute`sales`)で一語とし、語内でEntity(国内事業部)/Attribute(収入)を分割しない。
5. 主語が複数ある場合は、それぞれにアノテーションを行う。
   * 例示、列挙については各語をTargetとする: *「エビやかまぼこの売上が上がった」 => エビ、かまぼこ双方がTarget*
   * 代表例の提示については、例示の方が主体か、その後の集合の方が主体か、文脈から判断する: *「ワンピースやNARUTOといった、日本アニメコンテンツの販売が好調だった。」=>日本アニメコンテンツ全体ではなく、ワンピース、NARUTOが好調の主体と思える。これに対し、ワンピースやNARUTOを含む、日本アニメコンテンツの販売が好調だった。」場合、日本アニメコンテンツが主体となる*。
   * ・や、でつなげられているもので、独立しているものは分割する(「エビ・タイは何れも好調だった=>「エビ」「タイ」)。ただし、「麺・米飯類など」というように「麺・米飯類」で一語になっている場合(「麺・米飯類」)は分割しない
   * 語尾が「など/等/全体」で終わる場合(「冷凍魚・エビなど」)についても、分割を行い、など/等/全体はとる。
6. なお、個別でなく同一の`Target`が複数回登場する場合は、より具体的な表現、最初に登場したものを優先する
   * 具体的な記述を優先する: *「金融商品部門での売上はマイナスとなったが、これは同部門における人件費の高騰が理由である」=>「金融商品部門」「同部門」では、具体的な「金融商品部門」を優先*
   * 同一の具体性の場合、初出を優先する: *「**ガンバル**の売り上げは向上したため、ガンバルの利益もまた向上しました」=>同一の具体性であれば、最初に登場したガンバルをTargetとみなす*


## アノテーションデータフォーマット

### 個別アノテーション

個別のアノテーション結果については、以下のようなフォーマットで保存する。
保存は、文章ごと(企業ごと)にフォルダを作りその中に`ann__(企業のid)__(target_id)__(annotator_id).json`の形式で保存する。

```json
{
  "annotations": [
    {
      "target_id": "0",
      "target": "当連結会計年度におけるわが国経済は、政府の経済政策や日銀の金融緩和策により、企業業績、雇用・所得環境は改善し、...",
      "label": "NULL#general,neutral",
      "label_target": "わが国経済",
      "position": [
        11,
        16
      ],
      "annotator": "icoxfog417"
    },
    {
      "target_id": "0",
      "target": "当連結会計年度におけるわが国経済は、政府の経済政策や日銀の金融緩和策により、企業業績、雇用・所得環境は改善し、...",
      "label": "NULL#general,positive",
      "label_target": "企業業績",
      "position": [
        38,
        42
      ],
      "annotator": "icoxfog417"
    },...
  ]
}
```

| Parameter    | Type       | Description                                                                                 |
|--------------|------------|---------------------------------------------------------------------------------------------|
| **annotations**  | array[obj] | 各アノテーターのアノテーション結果を収めた配列                                              |
| target_id    | int        | アノテーション対象文章に含まれる各文に、一意に振られたid(連番)                              |
| target       | str        | アノテーション対象の文                                                                      |
| label        | str        | アノテーション結果。"Entity#Attribute,polarity"の形で付与される(ex: company#sales,positive) |
| label_target | str        | polarityの対象となっているEntity("ガンバル株式会社"など)                                    |
| position     | array[int] | targetにおける、label_targetの開始/終了位置                                                 |
| annotator    | str        | アノテーターのid                                                                            |

### 集計後アノテーション

個別のアノテーション結果を集計した、最終的なデータのフォーマットは以下のように保存する。
ファイル名は、`(企業のid)_ann.json`で、各企業ごと一つのファイルにまとめられる。

```json
{
  "header": {
    "document_id": "E00008",
    "document_name": "ホクト株式会社",
    "doc_text": "有価証券報告書",
    "edi_id": "E00008",
    "security_code": "13790",
    "category33": "水産・農林業",
    "category17": "食品",
    "scale": "6"
  },
  "sentences": [
    {
      "sentence_id": 0,
      "sentence": "当連結会計年度におけるわが国経済は、政府の経済政策や日銀の金融緩和策により、企業業績、雇用・所得環境は改善し...",
      "opinions": [
        {
          "target": "わが国経済",
          "category": "NULL#general",
          "polarity": "neutral",
          "from": 11,
          "to": 16
        },
        {
          "target": "企業業績",
          "category": "NULL#general",
          "polarity": "positive",
          "from": 38,
          "to": 42
        },...
      ],
    },
    {
      "sentence_id": 1,
      "sentence": "当社グループを取り巻く環境は、実質賃金が伸び悩むなか、消費者の皆様の...",
      "opinions": [
        {
          "target": "実質賃金",
          "category": "NULL#general",
          "polarity": "negative",
          "from": 15,
          "to": 19
        },...
      ]
    },...
  ]
}
```

| Parameter     | Type | Description                  |
|---------------|------|------------------------------|
| header   | obj  | アノテーション対象文書のヘッダー情報 |
| **sentences** | array[obj]  | 文書内の各文に行われたアノテーション結果 |

### header

| Parameter     | Type | Description                  |
|---------------|------|------------------------------|
| document_id   | str  | 一意の文書id(edi_idと等しい) |
| document_name | str  | 文書名(=企業名)              |
| doc_text      | str  | 文書種別名                   |
| edi_id        | str  | 企業のEDINETコード           |
| security_code | str  | 企業の証券コード             |
| category33    | str  | 企業の33業種区分             |
| category17    | str  | 企業の17業種区分             |
| scale         | str  | 企業の規模区分               |

### sentences

| Parameter   | Type       | Description                      |
|-------------|------------|----------------------------------|
| sentence_id | int        | 文書内の各文に振られた文id       |
| sentence    | str        | アノテーション対象の文           |
| **opinions**    | array[obj] | アノテーションの配列             |
| target      | str        | polarityの対象となっているEntity |
| category    | str        | Entity#Attributeのラベル         |
| polarity    | str        | polarityのラベル                 |
| from        | int        | targetの開始位置                 |
| to          | int        | targetの終了位置                 |
