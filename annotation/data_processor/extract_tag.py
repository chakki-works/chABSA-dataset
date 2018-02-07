import os
import argparse
from collections import OrderedDict
from bs4 import BeautifulSoup
from tqdm import tqdm


DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/raw/xbrls")
EXTRACTED_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/raw/extracted-htmls")


def get_xbrl_file(target_dir):
    xbrl_file = ""
    if os.path.isdir(target_dir):
        for f in os.listdir(target_dir):
            if f.endswith(".xbrl"):
                xbrl_file = os.path.join(target_dir, f)
    return xbrl_file


def get_tag(root, tag, as_html=False):
    n = root.find(tag)
    if n is None:
        return ""
    else:
        text = n.text.strip()
        if not as_html:
            text = text.replace("\r\n", " ").replace("\n", " ")
        else:
            text = text.replace("&lt;", "<").replace("&gt;", ">")
            try:
                html = BeautifulSoup(text, "html.parser")
                text = str(html)
            except Exception as ex:
                text = ""

        return text


def main(data_root, extracted_folder, tag_name):
    print("Now extract {}".format(tag_name))
    xbrl_paths = [get_xbrl_file(os.path.join(data_root, _dir)) for _dir 
                  in os.listdir(data_root) if _dir.startswith("E")]
    xbrl_paths = [p for p in xbrl_paths if p]

    meta_tags = OrderedDict([
        ("edi_code", "jpdei_cor:EDINETCodeDEI"),
        ("security_code", "jpdei_cor:SecurityCodeDEI"),
        ("company_name", "jpdei_cor:FilerNameInJapaneseDEI"),
        ("document_code", "jpdei_cor:IdentificationOfDocumentSubjectToAmendmentDEI"),
        ("document_title", "jpcrp_cor:DocumentTitleCoverPage"),
        ("fiscal_start_ymd", "jpdei_cor:CurrentFiscalYearStartDateDEI"),
        ("fiscal_end_ymd", "jpdei_cor:CurrentFiscalYearEndDateDEI"),
        ("document_format", "jpdei_cor:DocumentTypeDEI")
    ])  # use array to keep order

    metas = []
    print("Begin extraction...")
    for p in tqdm(xbrl_paths):
        meta = OrderedDict()
        body = ""
        with open(p, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml-xml")

            # get meta data
            for tag in meta_tags:
                text = get_tag(soup, meta_tags[tag])
                meta[tag] = text            
            if not meta["edi_code"]:
                print("The file {} is skipped because no EDI-CODE found.".format(
                      os.path.basename(p)))
                continue

            # get body text
            tags = tag_name.split(",")
            body = ""
            for t in tags:
                body += get_tag(soup, t, as_html=True)

            if not body:
                print("The file {} is skipped because '{}' is not found for not formatted.".format(
                    os.path.basename(p), tag_name))
                continue

            # save body file
            body_folder = meta["edi_code"].upper()
            body_path = os.path.join(EXTRACTED_FOLDER, body_folder)
            if not os.path.exists(body_path):
                os.mkdir(body_path)
            body_file_name = "tag.html"
            with open(os.path.join(body_path, body_file_name), mode="w", encoding="utf-8") as f:
                f.write(body)

            # append header info
            meta = list(meta.values()) + [os.path.join(body_folder, body_file_name)]
            metas.append(meta)

    meta_file_path = os.path.join(EXTRACTED_FOLDER, "companies.csv")
    with open(meta_file_path, mode="w", encoding="utf-8") as f:
        for m in metas:
            line = "\t".join(m) + "\n"
            f.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                description="Extract target tag from xbrl files.")
    parser.add_argument("--tag", type=str,
                        default="OverviewOfBusinessResultsTextBlock",
                        help="extract tag name")
    parser.add_argument("--file", type=str,
                        help="text file of tag list")

    args = parser.parse_args()
    # tag_name = "jpcrp_cor:OverviewOfBusinessResultsTextBlock"
    tag_name = "jpcrp_cor:" + args.tag
    if args.file:
        blocks_file = os.path.join(os.path.dirname(__file__), args.file)
        with open(blocks_file, encoding="utf-8") as f:
            lines = f.readlines()
            lines = [ln.strip() for ln in lines if ln.strip()]
            lines = ["jpcrp_cor:" + ln for ln in lines]
            tag_name = ",".join(lines)

    if not os.path.exists(EXTRACTED_FOLDER):
        # if folder is already exist, the file is overwrite/added to extracted folder
        os.mkdir(EXTRACTED_FOLDER)

    main(DATA_FOLDER, EXTRACTED_FOLDER, tag_name)
