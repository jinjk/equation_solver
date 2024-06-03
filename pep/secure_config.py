from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import yaml
from getpass import getpass

config = None

def gen_fernet_key(pwd:str) -> bytes:
    password = pwd.encode()
    salt = '+6u934mwrWZ7x+7UvMYbSA=='
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=base64.b64decode(salt),
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt(str, passwd):
    f = Fernet(gen_fernet_key(passwd))
    return f.encrypt(str.encode()).decode()

def decrypt(str, passwd):
    f = Fernet(gen_fernet_key(passwd))
    return f.decrypt(str.encode()).decode()

# read yaml file 'config.yaml' into a map
def read_config():
    global config
    if config:
        return config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    password = getpass()
    if ('tencent.ocr' in config):
        if ('secret_id' in config['tencent.ocr']):
            config['tencent.ocr']['secret_id'] = decrypt(config['tencent.ocr']['secret_id'], password)
        if ('secret_key' in config['tencent.ocr']):
            config['tencent.ocr']['secret_key'] = decrypt(config['tencent.ocr']['secret_key'], password)
    return config['tencent.ocr']

if __name__ == '__main__':
    read_config()