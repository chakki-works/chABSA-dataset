import os
import shutil
import re
import unicodedata
import MeCab
from bs4 import BeautifulSoup
from tqdm import tqdm


DATA_DIR = os.path.join(os.path.dirname(__file__),
                        "../../data/raw/extracted-htmls")


def main():
    symbols = re.compile(r"[^ぁ-んァ-ン一-龥ーa-zA-Zａ-ｚＡ-Ｚ0-9０-９]")
    numbers = re.compile(r"[0-9０-９]")
    start_with_number = re.compile(r"^[0-9０-９]+?")
    tagger = MeCab.Tagger("-Ochasen")
    company_file = os.path.join(DATA_DIR, "companies.csv")

    def tokenize_line(text):
        _txt = unicodedata.normalize("NFKC", text.strip()).lower()
        _txt = _txt.replace("\n", " ")
        _txt = numbers.sub("0", _txt)
        _txt = symbols.sub(" ", _txt).strip()
        _txt = start_with_number.sub("", _txt)
        node = tagger.parseToNode(_txt)
        tokens = []
        while node:
            if node.surface:
                pos = node.feature.split(",")
                if pos[0] == "名詞-数詞":
                    tokens.append(0)
                tokens.append(node.surface.strip())
            node = node.next
        tokens = [t for t in tokens if t]
        return " ".join(tokens)

    text_path = os.path.join(DATA_DIR, "../extracted-txts")
    if os.path.exists(text_path):
        print("Delete existed text dir.")
        shutil.rmtree(text_path)
    os.mkdir(text_path)

    print("Begin extraction...")
    with open(company_file, encoding="utf-8") as f:
        lines = f.readlines()
        tokens = [ln.strip().split("\t") for ln in lines]
        edi_paths = [(t[0], t[-1]) for t in tokens]

    for code, path in tqdm(edi_paths):
        html_file = os.path.join(DATA_DIR, path)
        soup = None

        # read html
        with open(html_file, encoding="utf-8") as f:
            content = f.read().strip()
            try:
                soup = BeautifulSoup(content, "html.parser")
            except Exception as ex:
                pass
        if soup is None:
            continue

        # get text lines
        for br in soup.find_all("br"):
            br.replace_with("\n")

        lines = []
        for c in soup.contents:
            valid = False
            if c.name:
                tag_name = c.name.lower()
                if tag_name.startswith("h"):
                    valid = True
                elif tag_name in ["span", "p"]:
                    valid = True
            if not valid:
                continue

            line = c.get_text().strip()
            if line:
                tokenized = tokenize_line(line)
                lines.append(tokenized)

            txt_path = os.path.join(text_path, code.lower() + ".txt")
            with open(txt_path, mode="w", encoding="utf-8") as f:
                f.write("\n".join(lines))


if __name__ == "__main__":
    main()
