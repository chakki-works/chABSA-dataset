import os
import sys
import json
from tqdm import tqdm
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from annotation.application.document import Document
from annotation.application.aspect_sentiment_task import AspectSntimentTask


DATA_DIR = os.path.join(os.path.dirname(__file__),
                        "../../data/interim/")

ANNOTATED_DIR = os.path.join(os.path.dirname(__file__),
                             "../../data/annotated/")

PROCESSED_DIR = os.path.join(os.path.dirname(__file__),
                             "../../data/processed/")

ADDITIONAL_INFO = os.path.join(os.path.dirname(__file__),
                             "additionals/edi_security_list.csv")


def add_additionals(annotated):
    if not hasattr(add_additionals, "additionals"):
        add_additionals.additionals = {}
        with open(ADDITIONAL_INFO, encoding="utf-8") as af:
            header = True
            for ln in af:
                if header:
                    header = False
                    continue
                tokens = ln.strip().split(",")
                tokens = [t.strip() for t in tokens]
                del tokens[2]  # drop company name
                key = tokens[0]
                add_additionals.additionals[key] = tokens[1:]

    key = annotated["header"]["document_id"]
    additionals = {}
    for i, a in enumerate(["security_code", "category33", "category17", "scale"]):
        additionals[a] = None
        if key in add_additionals.additionals:
            additionals[a] = add_additionals.additionals[key][i]

    annotated["header"].update(additionals)
    return annotated


def main():
    for doc in tqdm(sorted(os.listdir(DATA_DIR))):
        path = os.path.join(DATA_DIR, doc)
        if os.path.isfile(path) and doc.lower().startswith("e"):
            name, _ = os.path.splitext(doc)
            name = name.upper()
            annotated = read_annotated(name)
            if annotated is None:
                continue
            annotated = add_additionals(annotated)
            path = os.path.join(PROCESSED_DIR, name.lower() + "_ann.json")
            if annotated:
                with open(path, mode="w", encoding="utf-8") as f:
                    json.dump(annotated, f, ensure_ascii=False, indent=2)


def read_annotated(doc_name):
    annotated_dir = os.path.join(ANNOTATED_DIR, doc_name)
    if not os.path.exists(annotated_dir):
        return None

    doc_path = os.path.join(DATA_DIR, doc_name.lower() + ".jsonl")
    if not os.path.isfile(doc_path):
        return None

    doc = Document.load(doc_path)
    task = AspectSntimentTask.load(ANNOTATED_DIR, doc)
    header = doc.get_header()

    body = []
    for target_id, target in task.get_targets():
        o_s = []
        if target_id in task.annotations:
            distinct = {}
            for a in task.annotations[target_id]:
                a_dict = a.dumps()
                a_dict.pop("annotator")  # ignore annotator
                key = json.dumps(a_dict)
                distinct[key] = a

            for k in distinct:
                a = distinct[k]
                ea, s = a.label.split(",")
                o_s.append({
                    "target": a.label_target,
                    "category": ea,
                    "polarity": s,
                    "from": a.position[0],
                    "to": a.position[1]
                })

        body.append({
            "sentence_id": target_id,
            "sentence": target,
            "opinions": o_s
        })

    data = {
        "header": header,
        "sentences": body
    }

    return data


if __name__ == "__main__":
    main()
