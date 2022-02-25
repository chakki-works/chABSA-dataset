import re
import os
import mmap
import json
from tqdm import tqdm
from bs4 import BeautifulSoup


COMPANY_DATA_DIR = os.path.join(os.path.dirname(__file__), 
                                "../../data/raw/extracted-htmls/")


EXTRACTED_DATA_DIR = os.path.join(os.path.dirname(__file__), 
                                "../../data/interim/")


class Pattern():
    SUPPLEMENT_PATTERN = re.compile(r"(\(|（).+?(\)|）)")
    CHARACTER_PATTERN = re.compile(r"[^ぁ-んァ-ン一-龥ー]")
    RESULT_PATTERN = re.compile(r"^(連結)?業績(連結|の概要|の状況|の概況)?$")
    RESULT_SPECIALS = ["経営成績に関する分析", "当期の概況", "業績総括","連結会社の状況",
                       "当連結会計年度の業績", "当年度の概況", "企業集団の業績", 
                       "当行グループの業績", "事業の経過及びその成果", "全体の概況"]
    CASH_FLOW_PATTERN = re.compile(r"^(当期の|当年度の)?(連結)?キャッシュフロー(状況|の状況|の概況|関係)?(に関する分析|の分析)?$")
    CASH_FLOW_SPECIALS = ["財政状態に関する分析", "当期末の資産負債純資産及び当期のキャッシュフロー",
                          "連結貸借対照表"]

    @classmethod
    def wash_text(cls, text):
        if "\n" in text:
            _txt = text.split("\n")[0]
        else:
            _txt = text
        _txt = _txt.replace("－", "ー")
        _txt = cls.SUPPLEMENT_PATTERN.sub("", _txt)  # delete inner content of ()
        if len(_txt) == 0:
            _txt = text  # all text in ()
        _txt = cls.CHARACTER_PATTERN.sub("", _txt)
        return _txt

    @classmethod
    def get_category(cls, text):
        washed = cls.wash_text(text)
        if cls.RESULT_PATTERN.match(washed) or washed in cls.RESULT_SPECIALS:
            return "業績"
        elif cls.CASH_FLOW_PATTERN.match(washed) or washed in cls.CASH_FLOW_SPECIALS:
            return "キャッシュフローの状況"
        else:
            return ""


def read_html_file(rel_path, debug=False):
    html_file = os.path.join(COMPANY_DATA_DIR, rel_path)

    with open(html_file, encoding="utf-8") as f:
        content = f.read().strip()
    return read_html(content, debug)


def read_html(content, debug=False):
    soup = BeautifulSoup(content, "html.parser")
    for br in soup.find_all("br"):
        br.replace_with("\n")

    categories = []
    category_level = -1
    category_topics = {}
    topic = ""
    descriptions = []
    docs = []

    def add_doc(descs, category, topic):
        docs.append({"lines": descs, "category": category, "topic": topic})

    for c in soup.contents:
        if not c.name:
            continue

        text = c.get_text().strip()
        tag_name = c.name
        washed = Pattern.wash_text(text)

        if washed == "業績等の概要":
            continue

        if debug:
            print(text)
        category = Pattern.get_category(text)
        if category:
            if len(categories) > 0:
                add_doc(descriptions, categories[-1], topic)
            categories.append(category)
            category_topics[category] = []
            if category_level < 0 and tag_name.startswith("h"):
                category_level = int(tag_name[-1])
            topic = ""
            descriptions = []
        elif tag_name == "h" + str(category_level + 1) and len(washed) < 20:
            add_doc(descriptions, categories[-1], topic)
            topic = washed
            category_topics[categories[-1]].append(washed)
            descriptions = []
        elif tag_name in ["p", "span"] or tag_name.startswith("h"):
            if len(categories) == 0:
                categories.append("業績")
                category_topics["業績"] = []
            descriptions.append(text.strip())

    if len(descriptions) > 0:
        add_doc(descriptions, categories[-1], topic)

    return docs, category_topics


def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1
    return lines


def main():
    master_file = os.path.join(COMPANY_DATA_DIR, "companies.csv")
    count = 0
    with open(master_file, encoding="utf-8") as f:
        for line in tqdm(f, total=get_num_lines(master_file)):
            edi_id, s_code, company_name, doc_id, doc_text, fs_ymd, fe_ymd, d_fmt, file_path = line.strip().split("\t")
            debug = False

            if edi_id in ["E04762", "E11701", "E01950", "E04430", "E03618", "E01737"]:
                # E04762 オリックス株式会社 / 業績の記載なし
                # E11701 株式会社日本政策投資銀行 / 業績に該当しない情報を書きすぎ
                # E01950 株式会社アドバンテスト / 記載省略
                # E04430 日本電信電話株式会社 / 記載省略
                # E03618 株式会社ほくほくフィナンシャルグループ / 段落なし
                # E01737 株式会社日立製作所 / 記載省略
                continue
            
            doc, topic = read_html_file(file_path, debug)

            c = {
                "doc_id": edi_id,
                "doc_text": doc_text,
                "edi_id": edi_id,
                "company_name": company_name,
                "body": doc,
                "topic": topic
            }
            if len(topic.keys()) != 2:
                print(topic)
                if edi_id in ["E02881", "E03770", "E01570", "E02712", "E03138", "E00446", "E04353"]:
                    print("Different Format Company")
                    # 業績のみの記載
                    # E02881: 日本ライフライン株式会社
                    # E03770: 澤田ホールディングス株式会社
                    # E01570: ダイキン工業株式会社
                    # E02712: ＣＢグループマネジメント株式会社
                    # E03138: 株式会社オートバックスセブン
                    # E00446: 株式会社ニチレイ
                    # E04353: 株式会社サンリツ
                    pass
                else:
                    raise Exception("Can't parse the document of {} (done {})".format(
                        edi_id, count))
            
            file_name = edi_id.lower() + ".jsonl"
            with open(os.path.join(EXTRACTED_DATA_DIR, file_name), "w", encoding="utf-8") as f:
                json.dump(c, f, ensure_ascii=False, indent=2)
            count += 1


if __name__ == "__main__":
    if not os.path.exists(EXTRACTED_DATA_DIR):
        # if folder is already exist, the file is overwrite/added to extracted folder
        os.mkdir(EXTRACTED_DATA_DIR)

    main()
