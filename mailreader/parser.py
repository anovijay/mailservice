# parser.py
import os
from email.message import Message
from typing import List
from utils.helpers import save_temp_file

class EmailParser:
    def extract_files(self, msg: Message) -> List[dict]:
        extracted = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                payload = part.get_payload(decode=True)
                path = save_temp_file(filename, payload)
                extracted.append({"filename": filename, "path": path})
        return extracted
