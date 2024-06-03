# download file using requests lib
import requests
import os
from secure_config import read_config

config = read_config()

url = 'https://book.pep.com.cn/1211001302181/files/mobile/{}.jpg?240229102150'
pages = (132, 133)

def download_file(url, local_filename):
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_imgs():
    for img in range(*pages):
        download_file(url.format(img), os.path.join('imgs', f'{img}.jpg'))

if __name__ == '__main__':
    download_imgs()
