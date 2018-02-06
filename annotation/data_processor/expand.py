import os
from pathlib import Path
import zipfile

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/raw")


def main():
    data_file = os.path.join(DATA_FOLDER, "2016-annual-report-xbrls.zip")
    folder_name, _ = os.path.splitext(data_file)

    if not Path(DATA_FOLDER).joinpath(folder_name).exists():
        with zipfile.ZipFile(data_file) as z:
            z.extractall(path=DATA_FOLDER)
    
    if Path(data_file).exists():
        os.remove(data_file)


if __name__ == "__main__":
    main()
