# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import unittest
from annotation.data_processor.extract_text import read_html


ORDINARY_HTML = """

<h3 class="smt_head2">１ 【業績等の概要】</h3>
<h4 class="smt_head3" style="padding-left:8.9pt;">(1) 業績</h4>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">当連結会計年度におけるわが国経済は、海外経済の回復に伴う企業収益の改善、原油価格上昇に伴うガソリンや灯油の大幅上昇を主因とした消費者物価の上昇など、緩やかな回復基調が続いております。また、雇用情勢も有効求人倍率が上昇を続けるなど、雇用所得環境の改善を背景にした個人消費の持ち直しについても回復の兆しがみられるようになりました。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">当社グループの属する業界も、健康意識の高まりが持続し、平成27年４月より食品の新たな機能性表示制度が始まる等大きな変革期を迎えました。但し、異業種を含む大手企業の新規参入など更なる競合激化は続いており、当社グループを取り巻く環境は依然として厳しいものとなっております。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">このような状況のなか、当社グループとしては、「伝統と技術と人材力を価値にする」をビジョンとして平成27年機能性表示制度開始直後の６月に販売を開始しました「ヘルスエイド®　シリーズ」が引き続き好調に推移したこと、また、機能性素材であるローズヒップ、サラシアといった当社独自の素材販売を強化することにより、売上高は、10,967百万円（前年同期比5.1％増）と前年同期と比べ535百万円の増収となりました。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">利益面においては、効率的なプロモーション活動及びコストダウン諸施策による原価率の低減により営業利益は、427百万円（前年同期比9.0％増）と前年同期と比べ35百万円の増益となりました。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">また、営業外損益を加えた経常利益は、443百万円（前年同期比8.5％増）と前年同期と比べ34百万円の増益となりました。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">さらには投資有価証券評価損59百万円等の特別損失を加えた税金等調整前当期純利益は、379百万円と前年同期と比べ34百万円の増益となり、法人税等並びに法人税等調整額を加えた親会社株主に帰属する当期純利益は、240百万円（前年同期比35.9％減）と前年同期と比べ135百万円の減益となりました。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">セグメントの業績を示すと、次のとおりであります。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">①　ヘルスケア事業</p>
<p class="smt_text5" style="text-indent:8.9pt;">当セグメントにおきましては、機能性表示食品「ヘルスエイド®　シリーズ」が引き続き順調に推移し、また機能性素材の販売強化により、売上高は、7,751百万円と前年同期と比べ411百万円の増収となりました。</p>
<p class="smt_text5" style="text-indent:8.9pt;">損益面では、回転率の悪い商品を評価減するなど在庫の整理をしましたが、効率的なプロモーション活動等により、当連結会計年度のセグメント利益は、51百万円と前年同期と比べ155百万円の増益となりました。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">②　カプセル受託事業</p>
<p class="smt_text5" style="text-indent:8.9pt;">当セグメントにおきましては、医薬品カプセルやその他の受託については前年並みに推移し、またフレーバーカプセルも引き続き順調に推移し、その結果、売上高は、3,191百万円と前年同期と比べ112百万円の増収となりました。</p>
<p class="smt_text5" style="text-indent:8.9pt;">損益面では、コストダウン諸施策による原価率の改善に努めた結果、当連結会計年度のセグメント利益は、497百万円と前年同期と比べ5百万円の増益となりました。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">③　その他</p>
<p class="smt_text5" style="text-indent:8.9pt;">当セグメントにおきましては、売上高は、24百万円と前年同期と比べ10百万円の増収となりました。</p>
<p class="smt_text5" style="text-indent:8.9pt;">損益面では、主には長期にわたる創薬事業の知財取得に費用を支出した結果、当連結会計年度のセグメント損失は、122百万円と前年同期と比べ125百万円の減益となりました。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p style="page-break-before:always; line-height:0.75pt; width:100%; font-size:0.75pt;"> </p>
<h4 class="smt_head3" style="padding-left:8.9pt;">(2) キャッシュ・フローの状況</h4>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">当連結会計年度における現金及び現金同等物は2,877百万円と前年同期と比べ1,291百万円の増加となりました。</p>
<p class="smt_text3" style="padding-left:17.8pt;text-indent:8.9pt;">当連結会計年度に係る区分ごとのキャッシュ・フローの状況は以下のとおりであります。</p>
<p class="smt_text2" style="padding-left:8.9pt;text-indent:8.9pt;">（営業活動によるキャッシュ・フロー）</p>
<p class="smt_text4" style="padding-left:26.7pt;text-indent:8.9pt;">営業活動による資金は、1,301百万円の増加（前連結会計年度は969百万円の増加）となりました。その主な変動要因は、税金等調整前当期純利益379百万円、減価償却費708百万円、返品調整引当金の増加113百万円、売上債権の増加171百万円、たな卸資産の減少377百万円、仕入債務の減少209百万円によるものであります。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p class="smt_text2" style="padding-left:8.9pt;text-indent:8.9pt;">（投資活動によるキャッシュ・フロー）</p>
<p class="smt_text4" style="padding-left:26.7pt;text-indent:8.9pt;">投資活動による資金は、227百万円の減少（前連結会計年度は440百万円の減少）となりました。その主な変動要因は、設備更新投資など有形固定資産の取得による支出189百万円、無形固定資産の取得による支出73百万円によるものであります。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
<p class="smt_text2" style="padding-left:8.9pt;text-indent:8.9pt;">（財務活動によるキャッシュ・フロー）</p>
<p class="smt_text4" style="padding-left:26.7pt;text-indent:8.9pt;">財務活動による資金は、216百万円の増加（前連結会計年度は442百万円の減少）となりました。その主な変動要因は長期借入による収入962百万円、長期借入金の返済による支出592百万円、配当金支払152百万円によるものであります。</p>
<p class="smt_text6" style="line-height:9pt;">　</p>
"""

NON_HEADER_HTML = """

<h3>１【業績等の概要】</h3>
<p style="margin-left: 14px; line-height: 21px; text-align: left">
<span style="font-size: 14px">(1) 業績(連結)</span>
</p>
<div style="margin-left: 48px">
<table cellpadding="0" cellspacing="0" style="table-layout: fixed; width: 409px">
<colgroup>
<col style="width: 157px"/>
<col style="width: 252px"/>
</colgroup>
<tbody>
<tr>
<td style="width: 156px; border-left: 1px solid transparent; border-right: 1px solid transparent"></td>
<td style="border-left: 1px solid transparent; border-right: 1px solid transparent"></td>
</tr>
<tr style="min-height: 27px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">売上高</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-right: 36px; text-align: right; text-indent: 28px">48,708(△2,840億円)</p>
</td>
</tr>
<tr style="min-height: 27px">
<td style="border-left: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">営業損益</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-right: 36px; text-align: right; text-indent: 28px">2,708(＋7,538億円)</p>
</td>
</tr>
<tr style="min-height: 27px">
<td style="border-left: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">継続事業税引前損益</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-right: 36px; text-align: right; text-indent: 28px">2,255(＋6,249億円)</p>
</td>
</tr>
<tr style="min-height: 27px">
<td style="border-left: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">当期純損益</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-right: 36px; text-align: right; text-indent: 28px">△9,657(△5,057億円)</p>
</td>
</tr>
</tbody>
</table>
</div>
<p style="margin-left: 60px; text-align: left">
<span style="font-size: 12px">(注)１．単位：億円、( )</span>内　前期比較、△はマイナスを表示</p>
<p style="margin-left: 60px; text-align: left">　　２．「当社株主に帰属する当期純損益」を当期純損益として表示しています(以下、同じ)。</p>
<p style="margin-left: 28px; line-height: 21px; text-align: left; text-indent: 14px"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">当期の世界経済は、米国で総じて堅調な成長が続き、ユーロ圏では、ドイツをはじめ緩やかな成長が続きました。中国では個人消費が堅調に推移する一方、石炭、鉄鋼業で生産や投資の調整が行われ、成長がやや減速しました。国際金融面では、６月に英国のEU離脱に関する国民投票の結果、ポンドが急落し、11月には米国大統領選の影響等により、ドル高、株高が進みました。国内経済は、雇用、所得の改善が続く中、消費は概ね底堅く、設備投資には持ち直しの動きがみられました。輸出は持ち直しに向かいました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">来期の世界経済は、米国で引き続き堅調な成長が続き、ユーロ圏でも緩やかな成長が続く中、中国で成長率がやや高まり、世界全体としても成長率は高まると見込まれます。日本経済も１％台半ばの成長になると見込まれます。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">こうした状況下、当社グループは全てのステークホルダーからの信頼回復に向け、「海外原子力事業のリスク遮断」、「財務基盤の早期回復と強化」、「東芝グループ組織運営の強化」に取り組み、このうち、「海外原子力事業のリスク遮断」につきましては、米国時間2017年３月29日に、ウェスチングハウスエレクトリックカンパニー社及びその米国関係会社並びに米国外の事業会社群の持株会社である東芝原子力エナジーホールディングス(英国)社が米国連邦倒産法第11章に基づく再生手続を開始したことに伴い、ウェスチングハウス社グループは2016年度通期決算から、当社連結対象から除外され、ウェスチングハウス社グループに係る経営成績は、連結損益計算書上、非継続事業として取り扱われることになりました。</span>
</p>
<p class="style_pb_after" style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">この結果、当社グループの売上高は、メモリとHDDの増収があったものの、円高による影響や、構造改革によるパソコン・テレビの事業規模縮小の影響もあり、全体としては前期比2,840億円減少し4兆8,708億円になりました。営業損益は、賞与減額等の緊急対策に加え、前年度には資産評価減、構造改革費用、不採算案件の引当等の一時的費用を計上した影響もあったことから、原子力発電システム以外の全ての事業において、対前期で改善し、特にメモリについてはさらに利益率の改善が進み、約20％の営業利益率を達成した結果、前期比7,538億円増加し2,708億円になりました。継続事業税引前損益は、前期比6,249億円増加の2,255億円になりました。当期純損益は、ウェスチングハウス社グループの米国連邦倒産法第11章に基づく再生手続きに伴う損失を非継続事業当期純損益に計上したことにより、前期比5,057億円減少の△9,657億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: left; text-indent: 14px">
<span style="font-size: 14px">事業の種類別セグメントの業績(連結)は、次のとおりです。</span>
</p>
<div style="margin-left: 42px">
<table cellpadding="0" cellspacing="0" style="table-layout: fixed; width: 579.000000000001px">
<colgroup>
<col style="width: 266.359985351563px"/>
<col style="width: 167.080017089844px"/>
<col style="width: 145.559997558594px"/>
</colgroup>
<thead>
<tr>
<td style="width: 265.359985351563px; border-left: 1px solid transparent; border-right: 1px solid transparent"></td>
<td style="width: 166.080017089844px; border-left: 1px solid transparent; border-right: 1px solid transparent"></td>
<td style="border-left: 1px solid transparent; border-right: 1px solid transparent"></td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: center">セグメント</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: center">売上高</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: center">営業損益</p>
</td>
</tr>
</thead>
<tbody>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">エネルギーシステムソリューション</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">9,749 (△　864： 92％)</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">△417 (＋  791)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">
<span style="font-size: 12px">インフラシステムソリューション</span>
</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">12,624 (△　905： 93％)</p>
</td>
<td style="border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">584 (＋<span style="font-weight: normal">  658</span>)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">リテール＆プリンティングソリューション</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">
<span style="font-weight: normal">5,077 (△　372： 93％)</span>
</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">163 (＋<span style="font-weight: normal">1,010</span>)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">ストレージ＆デバイスソリューション</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">
<span style="font-weight: normal">17,002 (＋1,243：108％)</span>
</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">2,470 (＋3,470)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">インダストリアルICTソリューション</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">
<span style="font-weight: normal">2,384 (△　184： 93％)</span>
</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">116 (＋   29)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">その他</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">
<span style="font-weight: normal">5,301 (△2,659： 67％)</span>
</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">△217 (＋1,603)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">消去</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">
<span style="font-weight: normal">△3,429 (＋　901： －  )</span>
</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">9 (△   23)</p>
</td>
</tr>
<tr style="min-height: 25.3299999237061px">
<td style="border-left: 1px solid #000000; border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="margin-left: 6px; text-align: left">合計</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">48,708 (<span style="font-weight: normal">△2,840</span>： 94％)</p>
</td>
<td style="border-top: 1px solid #000000; border-right: 1px solid #000000; border-bottom: 1px solid #000000; vertical-align: middle">
<p style="text-align: right">2,708 (＋7,538)</p>
</td>
</tr>
</tbody>
</table>
</div>
<p style="margin-left: 60px; text-align: left">(注)<span style="font-size: 12px">１．</span>単位：億円、( )内　前期比較、△はマイナスを表示</p>
<p style="margin-left: 106.669998168945px; line-height: 19.3299999237061px; text-align: left; text-indent: -22.6700000762939px"> </p>
<p style="margin-left: 106.669998168945px; line-height: 19.3299999237061px; text-align: left; text-indent: -22.6700000762939px"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">①エネルギーシステムソリューション</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　火力・水力発電システムが増収になったものの、原子力発電システム、送変電・配電システム等、ランディス・ギア社が減収になった結果、部門全体の売上高は前期比864億円減少し9,749億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　損益面では、原子力発電システムが悪化しましたが、火力・水力発電システム、送変電・配電システム等、ランディス・ギア社が大幅な増益になりました。これらの結果、部門全体の営業損益は前期比791億円改善し417億円の損失を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">②インフラシステムソリューション</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　各事業とも減収になり、部門全体の売上高は前期比905億円減少し１兆2,624億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　損益面では、各事業とも大幅な増益になったことにより、部門全体の営業損益は前期比658億円増加し584億円の利益を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">③リテール＆プリンティングソリューション</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　リテール事業は好調に推移しましたが、為替の影響により部門全体の売上高は前期比372億円減少し5,077億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　損益面では、前期は海外リテール事業の減損損失により赤字になりましたが、当期はリテール事業の収益改善により黒字化しました。これらの結果、部門全体の営業損益は前期比1,010億円増加し163億円の利益を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">④ストレージ＆デバイスソリューション</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　HDDが大幅な増収に、メモリも増収になった結果、部門全体の売上高は前期比1,243億円増加し１兆7,002億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　損益面では、各事業とも大幅な増益になったことにより、部門全体の営業損益は前期比3,470億円増加し2,470億円の利益を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">⑤インダストリアルICTソリューション</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　製造業向けシステム案件が減収になり、部門全体の売上高は前期比184億円減少し2,384億円になりました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">　緊急対策と収益改善施策により、部門全体の営業損益は前期比29億円増加し116億円の利益を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph"> </p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">⑥その他部門</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">部門全体の売上高は5,301億円になり、営業損益は217億円の損失を計上しました。</span>
</p>
<p style="margin-left: 28px; line-height: 21px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px"> </p>
<p style="margin-left: 28px; line-height: 21px; margin-bottom: 24px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-size: 14px">なお、上記の事業の種類別の売上高には、セグメント間の内部売上高又は振替高3,429億円が含まれています。</span>
</p>
<p style="margin-left: 14px; line-height: 21px; text-align: justify; text-justify: inter-ideograph">
<span style="font-size: 14px">(2) キャッシュ・フロー</span>
</p>
<p style="margin-left: 42px; line-height: 21px; margin-bottom: 7px; text-align: left; text-indent: 14px">
<span style="font-family: 'MS Mincho'; font-size: 14px">当期における営業活動によるキャッシュ・フローは、前期の12億円の支出から1,354億円改善し、1,342億円の収入になりました。</span>
</p>
<p style="margin-left: 42px; line-height: 21px; text-align: left; text-indent: 14px">
<span style="font-family: 'MS Mincho'; font-size: 14px">投資活動によるキャッシュ・フローは、前期において東芝メディカルシステムズ㈱の売却等があったことにより、前期の6,534億円の収入から8,324億円減少し、1,790億円の支出になりました。</span>
</p>
<p style="margin-left: 42px; line-height: 21px; text-align: left; text-indent: 14px">
<span style="font-family: 'MS Mincho'; font-size: 14px">これらの結果、当期のフリー・キャッシュ・フローは、前期の6,522億円の収入から6,970億円減少し、448億円の支出になりました。</span>
</p>
<p style="margin-left: 42px; line-height: 21px; text-align: left; text-indent: 14px">
<span style="font-family: 'MS Mincho'; font-size: 14px">財務活動によるキャッシュ・フローは、前期の1,357億円の収入から3,555億円キャッシュが減少し、2,198億円の支出になりました。</span>
</p>
<p style="margin-left: 42px; line-height: 21px; margin-bottom: 7px; text-align: justify; text-justify: inter-ideograph; text-indent: 14px">
<span style="font-family: 'MS Mincho'; font-size: 14px">その他に為替の影響によるキャッシュの減少が32億円あり、当期末の現金及び現金同等物の残高は、前期の9,755億円から2,678億円減少し、7,077億円になりました。</span>
</p>
<p style="margin-left: 66px; text-align: justify; text-justify: inter-ideograph; text-indent: -36px">(注)・連結財務諸表は、米国会計基準に準拠して作成しています。但し、当社グループの営業損益は、売上高から売上原価、販売費及び一般管理費並びにのれん減損損失を控除して算出したものであり、経営資源の配分の決定及び業績の検討のため、定期的に評価を行う対象となる損益を示しています。一部の事業構造改革費用及び訴訟和解費用等は、当社グループの営業損益には含まれていません。</p>
<p style="margin-left: 66px; text-align: justify; text-justify: inter-ideograph; text-indent: -36px">　　・ヘルスケア事業、家庭電器事業及び<span style="font-size: 12px">WECグループにおける原子力事業</span>は、Accounting Standards Codification 205-20 「財務諸表の表示―非継続事業」に従い、連結損益計算書上非継続事業として取り扱われるため、売上高、営業損益、継続事業税引前損益にはこれらの事業に係る経営成績は含まれていません。当社グループの当期純損益は、継続事業税引前損益にこれらの事業に係る経営成績を加減して算出されています。また、連結貸借対照表上も非継続事業として取り扱われるため、区別して表示しています。これに伴い、過年度の数値も組み替えて表示しています。</p>
<p style="text-align: left"> </p>
<p style="margin-left: 66px; text-align: left; text-indent: -36px"> </p>

"""


MULTIPLE_H_HTML = """

<h3 class="smt_head2" style="padding-left:9pt;">１【業績等の概要】</h3>
<h4 class="smt_head3" style="padding-left:0pt;">（１）業績</h4>
<h5 class="smt_head4" style="text-justify:inter-ideograph;text-indent:9.5pt;">当事業年度におけるわが国経済は、企業収益や雇用環境に改善が見られ緩やかな回復基調にあるものの、中国や新興国経済の減速懸念に加えて英国のＥＵ離脱問題や米国新政権の経済政策など世界経済の不確実性も高まり、先行きは不透明な状況が続きました。当社の属する医療衛生材料業界におきましては、人口減少に伴う国内マーケットの縮小に加え、国が推し進める医療費抑制施策を受けた医療機関の経費抑制による影響で価格競争が激化しており、引き続き厳しい事業環境が継続しております。</h5>
<h5 class="smt_head4" style="margin-bottom:10pt;text-justify:inter-ideograph;text-indent:9.5pt;">このような状況下で当社の当事業年度の業績は、売上高は22,990,519千円（前年同期比14.1%減少）、営業利益は17,256千円（同92.3%減少）、経常利益は33,149千円（同42.0%増加）、当期純利益は92,583千円（前年同期は503,112千円の当期純損失）となりました。</h5>
<p class="smt_text3" style="margin-top:10pt;margin-bottom:10pt;">セグメント別の業績は、次のとおりであります。なお、当事業年度より報告セグメントの区分を変更しており、前事業年度との比較・分析は変更後の区分に基づいて記載しております。</p>
<h5 class="smt_head4">（メディカル）</h5>
<h6 class="smt_head5" style="padding-left:18pt;text-justify:inter-ideograph;text-indent:9.5pt;">「感染予防関連製品」「口腔ケア製品」「手術関連製品」その他高付加価値製品・商品の販売拡充に努めました。しかしながら、前事業年度に実施した一部滅菌製品の自主回収による影響から完全に回復するまでには至らず、売上高は8,680,378千円（前年同期比26.0%減少）となりました。</h6>
<h6 class="smt_head5" style="padding-left:18pt;margin-bottom:10pt;text-justify:inter-ideograph;text-indent:9.5pt;">売上総利益率の確保に向けた営業施策の実行や前事業年度に実施した拠点集約化等による合理化効果、従業員の減少に伴う人件費減少、売上高の減少に伴う運賃等の販売経費減少等により、売上原価と販売費及び一般管理費の合計額を8,729,023千円（同23.5%減少）まで抑制したものの、売上高減少による生産稼働率の低下を補うまでには至らず営業損失は48,646千円（前年同期は323,231千円の営業利益）となりました。</h6>
<h5 class="smt_head4">（コンシューマ）</h5>
<h6 class="smt_head5" style="padding-left:18pt;text-justify:inter-ideograph;text-indent:9.5pt;">「口腔ケア製品」や一般消費者向け各種衛生材料及び医療用品等の製品に仕入商品を加えて、大手量販店や通信販売事業者など幅広い顧客に対し積極的に販売いたしました。しかしながら、前事業年度より好調を維持していたインバウンド需要の失速による影響を受けたことから、売上高は14,310,141千円（前年同期比4.8%減少）となりました。</h6>
<h6 class="smt_head5" style="padding-left:18pt;text-justify:inter-ideograph;text-indent:9.5pt;">利益面では、売上総利益率の低い商品の売上構成比が上昇したこと等の影響により、営業利益は642,061千円（同16.0%減少）となりました。</h6>
<p style="page-break-before:always; line-height:0.75pt; width:100%; font-size:0.75pt;"> </p>
<h4 class="smt_head3" style="padding-left:0pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-justify:inter-ideograph;text-indent:0pt;font-family:'ＭＳ 明朝';text-align:justify;letter-spacing:0pt;line-height:15pt;">（２）キャッシュ・フローの状況に関する分析</h4>
<p class="smt_text6" style="text-align:justify;padding-left:30pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">当事業年度末における現金及び現金同等物は前事業年度末より911,823千円減少し、2,215,869千円（前事業年度末は3,127,692千円）となりました。</p>
<p class="smt_text6" style="padding-left:30pt;margin-bottom:13.5pt;text-indent:10pt;">当事業年度における各キャッシュ・フローの状況と主な要因は、次のとおりであります。</p>
<p class="smt_text6" style="text-align:justify;padding-left:20pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">（営業活動によるキャッシュ・フロー）</p>
<p class="smt_text6" style="text-align:justify;padding-left:30pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">営業活動によるキャッシュ・フローは499,411千円（前年同期は△140,766千円）となり、前年同期と比べ640,178千円の収入増加で6期ぶりのプラスに転じました。</p>
<p class="smt_text6" style="padding-left:30pt;margin-bottom:10pt;text-indent:10pt;">これは、前事業年度に発生した一部滅菌製品の自主回収に関連する費用がなくなったこと等により税引前当期純損失が前年同期と比べ274,866千円（99.0%）減少したことに加え、前年同期の税引前当期純利益に含まれていた固定資産売却損益478,658千円や投資有価証券売却益52,297千円が当事業年度には発生しなかったことが主な要因です。</p>
<p class="smt_text6" style="text-align:justify;padding-left:20pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">（投資活動によるキャッシュ・フロー）</p>
<p class="smt_text6" style="text-align:justify;padding-left:30pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">投資活動によるキャッシュ・フローは993,840千円（前年同期は541,714千円）となり、前年同期と比べ452,125千円の収入増加となりました。</p>
<p class="smt_text6" style="padding-left:30pt;margin-bottom:10pt;text-indent:10pt;">これは、定期預金の預入による支出が前年同期と比べ1,490,617千円減少した一方で、当事業年度は有形固定資産の売却による収入が発生しなかった（前年同期は1,100,257千円）ことが主な要因です。</p>
<p class="smt_text6" style="text-align:justify;padding-left:20pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">（財務活動によるキャッシュ・フロー）</p>
<p class="smt_text6" style="text-align:justify;padding-left:30pt;padding-right:0pt;margin-top:0pt;margin-bottom:0pt;text-indent:10pt;font-family:'ＭＳ 明朝';letter-spacing:0pt;line-height:15pt;">財務活動によるキャッシュ・フローは△2,399,483千円（前年同期は△306,194千円）となり、前年同期と比べ2,093,288千円の支出増加となりました。</p>
<p class="smt_text6" style="padding-left:30pt;margin-bottom:22pt;text-indent:10pt;">これは、長期借入金の返済による支出が前年同期と比べ725,930千円増加した一方で、新規の資金調達を抑制したことにより長期借入れによる収入が発生しなかった（前年同期は1,500,000千円）ことが主な要因です。</p>
"""

class TestExtractText(unittest.TestCase):

    def test_ordinary_html(self):
        doc, topics = read_html(ORDINARY_HTML)
        self.assertEqual(len(doc), 2)  # 業績/キャッシュフロー
        self.assertEqual(len(topics.keys()), 2)
        for d in doc:
            print(d[1])
            print("\n".join(d[0]))
            print("===")

    def test_non_header_html(self):
        doc, topics = read_html(NON_HEADER_HTML)
        self.assertEqual(len(doc), 2)  # 業績/キャッシュフロー
        self.assertEqual(len(topics.keys()), 2)
        for d in doc:
            print(d[1])
            print("\n".join(d[0]))
            print("===")

    def test_multiple_header_html(self):
        doc, topics = read_html(MULTIPLE_H_HTML)
        self.assertEqual(len(topics.keys()), 2)
        for d in doc:
            print(d[1])
            print("\n".join(d[0]))
            print("===")
        self.assertEqual(len(doc), 4)  # 業績/業績+メディカル/業績+コンシューマ+キャッシュフロー
        self.assertEqual(len(topics["業績"]), 2)  # 業績+メディカル/業績+コンシューマ
        

if __name__ == "__main__":
    unittest.main()
