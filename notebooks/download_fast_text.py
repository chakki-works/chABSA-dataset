import os
from tqdm import tqdm
import requests


def main():
    path = os.path.join(os.path.dirname(__file__), "wiki.ja.vec")
    url = "https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki.ja.vec"

    r = requests.get(url, stream=True)
    chunk_size = 1024
    file_size = int(r.headers.get("content-length", 0)) / chunk_size
    if r.ok:
        with open(path, "wb") as f:
            for chunk in tqdm(r.iter_content(chunk_size=chunk_size),
                              total=file_size, unit="B", unit_scale=True):
                f.write(chunk)
    else:
        raise Exception("Can't download the file.")

    print("Downloaded the fastText vector!")


if __name__ == "__main__":
    main()
