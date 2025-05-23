# helpers.py
import os
import tempfile
import hashlib
import logging

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def save_temp_file(filename, content):
    path = os.path.join(tempfile.gettempdir(), filename)
    with open(path, "wb") as f:
        f.write(content)
    return path

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()
