# アノテーション仕様書

Reference from [SemEval-2016 Task 5](http://alt.qcri.org/semeval2016/task5/data/uploads/absa2016_annotationguidelines.pdf)

# アノテーションの概要

有価証券報告書について、極性(polarity)、およびその対象(Entity)と属性(Attribute)をアノテーションする。

例: 株式会社ガンバルの売り上げは、好調だった。

* Entity: 株式会社ガンバル
* Attribute: 売り上げ
* polarity: positive

この場合、`company#sales, positive`といった形でアノテーションされる。

# アノテーションの種類について

Entity、およびAttributeの種類については以下となる。

Entity

* market: 市場
* company: 会社
* business: 事業
* product: 製品/サービス

Attribute

* sales: 売上
* profit: 利益
* amount: 販売数量
* price: 販売単価
* cost: 原価

positive/negativeの判定が可能だが、Entity/Attributeが不明、欠損、上記で定義されたものではない場合について

* Entityなし、Attributeあり => Entityに`NULL`を指定する。
  * 例: 「売上高は15%増加しました」 `sales`の判定が可能だが、Entityがない
* Entityあり、Attributeなし => Attributeに`general`を付与する。
  * 例: 「地方物産事業部は好調でした」`business`の判定が可能だが、Attributeがない
* Entityなし、Attributeなし => Entityに`NULL`(out of domain)、Attributeに`general`でアノテーションする。
  * 例: 「わが国の経済は引き続き厳しい状況でした」 EntityもAttributeもないがセンチメントの判定が可能(わが国の経済/厳しい状況)=`NULL#general, negative`

なお、sentimentが読み取れるがpositiveともnegativeとも言えない場合`neutral`を付与する。
一文に、同じEntityに対し複数のAttributeが登場する場合は同じEntityに対し複数回アノテーションを行う。

* 株式会社ガンバルの売り上げ、利益はともに向上した
  * 株式会社ガンバル/売り上げ/向上した: `company#sales, positive`
  * 株式会社ガンバル/利益/向上した: `company#profit, positive`

## Examples

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

# アノテーション基準について

結果のみを対象にする

* x: 国内事業の売り上げ増加に取り組みました=>取り組んだだけで、結果どうなったかはわからない
  * 実現していない活動: 強化します、改善に取り組みましたetc
  * 実現していない未来、予測: 上向く予定です、改善「傾向」にあります、下振れさせるリスク、懸念etc
* o: 国内事業の売上は増加しました

それ自体が極性を持たないものは対象としない。

* x: 社会構造の変化、金融資本市場の変動、消費者の皆様の生活防衛意識の高まりや節約志向
  * これらは、それ自体はpositiveでもnegativeでもない

文単位でアノテーションを行う。前後の文脈からpositiveだと推定できても、その文ではnegativeならnegativeとする。
アノテーションは、EntityとAttributeの組み合わせで行う。事業の売り上げが悪い、というは場合`business#sales,negative`といった形になる。
Entity、Attributeの一覧は以下。

Entityは固有表現、また空白で区切る場合は連結名詞として認識できるものに付与する(=「の」などで連携されるものは対象とならない)。

* インドでの販売が、下半期に入り高額紙幣切り替えの影響で一時的に減少しました
  * Entity「販売」が「減少」(「インドでの販売」ではない)
* 国内、中国、EMEAの中小型の減・変速機の市況
  * 「市況」がEntity

## Entityについて

* Attributeの主語を取る
  * ex: 調理冷凍食品事業ではエビ加工品やかに風味かまぼこの販売が伸長しました->この場合、「販売が伸長」したのはエビ&カニ風味で、事業でない
* Entityが複数登場する場合は、最初のものを対象にする
  * 「**ガンバル**の売り上げは向上したため、ガンバルの利益もまた向上しました」=>最初の「ガンバル」をEntityとみなす
* 同一Entityに対する言及が複数ある場合は、最も具体的なものを採用する
  * 「金融商品部門での売上はマイナスとなったが、これは同部門における人件費の高騰が理由である」=>「金融商品部門」「同部門」は、「金融商品部門」を優先
* 1 Entityに対して、複数Attributeが存在する場合
  * 別々に付与する
  * ex: わが社の売上は増大したが、利益は減りました -> (company#sales, positive + company#profit, nagative)
* 粒度の異なるEntityが複数登場する場合、 基本的に最も具体的な記述を優先する
  * ex: 「ワンピースやNARUTOといった、日本アニメコンテンツの販売が好調だった。」=>ワンピース、NARUTO(not 日本アニメコンテンツ)
  * ただし、例示については、後ろの語が文中において主な意味を持つ場合は後ろの語を優先する
  * ex1: 「「ワンピース」及び「ドラゴンボール」シリーズのゲーム化権」⇒ゲーム化権。これはワンピースやドラゴンボールそのものではなく、その「ゲーム化権」が実際に扱っているものであるため。
  * ex2: 「Provoiceを含む音声合成ソリューション」⇒例示したProvoiceは一例に過ぎず、その総体である「音声合成ソリューション」の方が重要ともとれる。例示が「主要/重要な一部の提示」か、「集合の一例のピックアップのみ」かは文脈で判断する。
* 連語について
  * ・や、でつなげられているもので、独立しているものは分割する(「エビ・タイは何れも好調だった=>「エビ」「タイ」)。
  * 語尾が「など/等/全体」で終わる場合(「冷凍魚・エビなど」)についても、分割を行い、など/等/全体はとる。
  * 「麺・米飯類など」というように「麺・米飯類」で一語になっている場合(「麺・米飯類」)は分割しない
* 複合語について
  * 連続する名詞によって作られる名詞句は、それをEntityとして認識する
  * ex: 「国内きのこ事業」、「海外きのこ事業」など
  * 「xx収入」や「yy売上」は、エンティティとみなせる語を含んでいても分割しない()
* Entityがないが、Attributeはある場合
  * 「この結果、売上高は100円増加した」というように、その文内でEntityが述べられていない場合NULLを使用し、「売上高」にNULL#sales, positiveをつける
  * Attribute自体が主語であり、Attributeとは異なる主語が文中に現れる場合二つ付ける。
  * ex: 「セグメント利益は、電子部品向け金属粉の販売好調により、同186百万円増益（32.6％増益）の759百万円となりました」=>「セグメント利益」はNULL、「電子部品向け金属粉」は別主語

個別のEntityについて

* market: generalのみ。
  * 場合によって単価や需要についての言及があるが、それは「ｘｘ市場におけるｙｙの単価は下降気味で・・・」などEntityを伴う場合が多い。この場合のEntityは会社の製品ではなくmarketの製品のため意味合いが異なる。そのためタグ付けは行わない
* company: 会社以外に、グループなども対象とする
* product: サービス産業におけるサービスもproductの扱いとする(「貴金属めっき加工」など)
  
## Attributeについて 
  
* 分類区分に特に当たらないが、positive/negativeが判断できる場合はgeneralとする
  * ex:わが社の業績は堅調だった->company#general, positive
* 「前年並み」はneutralとする。文面の雰囲気で判断が可能な場合はそれに準ずる(前年並みに留まった、ならnegativeなど)
  * 明確にpositve/negativeを言っていない場合にのみneutralとする
* 「xx収入」や「yy売上」は、エンティティとみなせる場合は分割する
  * ex: 「広告事業収入が向上した」という場合、「広告事業/収入/向上」としてbusiness#sales, positiveとする
  * 「コスト増加」や「利益率低下」については、「`NULL#cost, negative`」「`NULL#profit, negative`」といった形で付与する

個別のAttributeについて

* amount: 販売数、生産量。「生産性」など単位が数量でなくなるものはgeneralに入れる。
  * 「需要」はamountではないので注意(売った量でも生産した量でもないため)
* price: 販売価格についての言及に付与する「原料価格」はcostに入るので注意
  * 「原料価格」はcostに入るので注意。仕入単価の高騰、といった使い方の場合もcost扱い
  * ex: 「かまぼこについては、原料魚の価格の高騰が発生しました」 -> product#cost, negative
  * ex: ただし、「かまぼこについては、原料魚の価格の高騰が発生し、販売減となりました」はかまぼこについて複数Attributeになるため、複数Attributeの定義に沿い最後尾のsalesがアノテーション対象となる。

# アノテーションデータフォーマット

## 個別アノテーション

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

## 集計後アノテーション

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
