# email_client.py
import imaplib
import email
from email.message import Message
from typing import List
from utils.helpers import log_info, log_error

class EmailClient:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = imaplib.IMAP4_SSL(self.config.EMAIL_SERVER, self.config.EMAIL_PORT)
            self.conn.login(self.config.EMAIL_USER, self.config.EMAIL_PASSWORD)
            self.conn.select("inbox")
            log_info("Connected to email server")
        except Exception as e:
            log_error(f"Failed to connect to email: {e}")
            raise

    def fetch_emails(self) -> List[Message]:
        self.connect()
        result, data = self.conn.search(None, '(UNSEEN)')
        if result != 'OK':
            log_info("No unread messages found.")
            return []

        emails = []
        for num in data[0].split():
            # imaplib returns message numbers as bytes, but the fetch command
            # expects a string. Passing bytes would result in a literal
            # representation like "b'1'" which fails. Decode to str first.
            num_str = num.decode()
            result, data = self.conn.fetch(num_str, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            emails.append(msg)

        self.conn.close()
        self.conn.logout()
        return emails
