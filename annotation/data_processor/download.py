import os
import requests
from tqdm import tqdm


DATA_FOLDER = os.path.join(os.path.dirname(__file__), "../../data/raw")


def main():
    url = "https://s3-ap-northeast-1.amazonaws.com/dev.tech-sketch.jp/chakki/public/2016-annual-report-xbrls.zip"
    r = requests.get(url, stream=True)
    if not r.ok:
        r.raise_for_status()
    
    data_file = os.path.join(DATA_FOLDER, os.path.basename(url))
    total_size = int(r.headers.get("content-length", 0))
    with open(data_file, "wb") as f:
        chunk_size = 1024
        limit = total_size / chunk_size
        for data in tqdm(r.iter_content(chunk_size=chunk_size),
                         total=limit, unit="B", unit_scale=True):
            f.write(data)


if __name__ == "__main__":
    main()
