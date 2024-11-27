import hashlib


def get_hash(value: str):
    return hashlib.sha256(value.encode()).hexdigest()
