import os
import shutil
from bs4 import BeautifulSoup


# This script is used to extract xbrl files from downloaded folder from EDINET
# http://disclosure.edinet-fsa.go.jp/


DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/raw")
XBRL_ROOT = os.path.join(os.path.dirname(__file__), "../../data/raw/xbrls")


def get_text(root, tag):
    n = root.find(tag)
    if n is None:
        return ""
    else:
        return n.text.strip().replace("\r\n", " ").replace("\n", " ")


def main(data_root, file_root):
    metadata = {}
    initial = True
    _dirs = [_dir for _dir in os.listdir(data_root)
             if os.path.isdir(os.path.join(data_root, _dir))]
    for i, _dir in enumerate(_dirs):
        searched_dir = os.path.join(data_root, _dir)
        for s_dir in os.listdir(searched_dir):
            s_dir_path = os.path.join(searched_dir, s_dir)
            if not os.path.isdir(s_dir_path):
                continue
            file_dir = os.path.join(s_dir_path, "XBRL/PublicDoc/")
            xbrl = [f for f in os.listdir(file_dir) if f.endswith(".xbrl")]
            xbrl_path = ""
            if len(xbrl) > 0:
                xbrl = xbrl[0]
                xbrl_path = os.path.join(file_dir, xbrl)
            else:
                raise Exception("XBRL file does not exist")

            copy = False
            edi_code = ""
            with open(xbrl_path, encoding="utf-8") as f:
                soup = BeautifulSoup(f, "lxml-xml")
                edi_code = get_text(soup, "jpdei_cor:EDINETCodeDEI")
                s_code = get_text(soup, "jpdei_cor:SecurityCodeDEI")
                c_name = get_text(soup, "jpdei_cor:FilerNameInJapaneseDEI")
                d_code = get_text(soup, "jpdei_cor:IdentificationOfDocumentSubjectToAmendmentDEI")
                d_title = get_text(soup, "jpcrp_cor:DocumentTitleCoverPage")
                f_start_ymd = get_text(soup, "jpdei_cor:CurrentFiscalYearStartDateDEI")
                f_end_ymd = get_text(soup, "jpdei_cor:CurrentFiscalYearEndDateDEI")
                d_format = get_text(soup, "jpdei_cor:DocumentTypeDEI")

                if "有価証券報告書" not in d_title:
                    continue

                if edi_code in metadata:
                    continue
                
                print("Record {}:{} {}".format(edi_code, s_code, c_name))

                metadata[edi_code] = (
                    edi_code,
                    s_code,
                    c_name,
                    f_start_ymd,
                    f_end_ymd,
                    d_code,
                    d_title,
                    d_format,
                    "/".join([file_root, edi_code, xbrl])
                )
                copy = True
            
            if copy:
                company_dir = os.path.join(file_root, edi_code)
                if not os.path.exists(company_dir):
                    os.mkdir(company_dir)
                    shutil.copyfile(xbrl_path, os.path.join(company_dir, xbrl))
    
    metadata_file = "companies.csv"
    with open(metadata_file, mode="w", encoding="utf-8") as f:
        for k in metadata:
            f.write("\t".join(metadata[k]) + "\n")


if __name__ == "__main__":
    if not os.path.exists(XBRL_ROOT):
        os.mkdir(XBRL_ROOT)
    main(DATA_FOLDER, XBRL_ROOT)
