import os
from collections import Counter
import json


ANNOTATE_DIR = os.path.join(os.path.dirname(__file__), "../../data/annotated")


def print_counter(c):
    result = c.most_common()
    result_dict = dict(result)
    string = json.dumps(result_dict, ensure_ascii=False, indent=2, sort_keys=True)
    print(string)


def main():
    s_counter = Counter()
    e_counter = Counter()
    ea_counter = Counter()
    label_collection = {}
    total = 0
    for _dir in os.listdir(ANNOTATE_DIR):
        if not _dir.startswith("E"):
            continue
        
        company_dir = os.path.join(ANNOTATE_DIR, _dir)
        for a in os.listdir(company_dir):
            if not a.startswith("ann"):
                continue
            path = os.path.join(company_dir, a)
            with open(path, encoding="utf-8") as f:
                af = json.load(f)
                ass = af["annotations"]
                for a in ass:
                    label = a["label"]
                    ea, s = label.split(",")
                    e, at = ea.split("#")
                    if label not in label_collection:
                        label_collection[a["label"]] = []
                    label_collection[a["label"]].append(a["label_target"])
                    s_counter[s] += 1
                    ea_counter[ea] += 1
                    e_counter[e] += 1
                    total += 1

    display = json.dumps(label_collection, ensure_ascii=False, indent=2, sort_keys=True)
    print(display)
    print_counter(ea_counter)
    print_counter(s_counter)
    print_counter(e_counter)
    print(total)
            

if __name__ == "__main__":
    main()
