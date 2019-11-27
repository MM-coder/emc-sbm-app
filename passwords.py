import hashlib

def hash_plain_text(string: str):
    hash_object = hashlib.md5(string.encode())
    return hash_object.hexdigest()