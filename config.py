import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "test")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER", "imap.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
    GCS_BUCKET = os.getenv("GCS_BUCKET", "rhea_incoming_files")
    EVENT_TOPIC = os.getenv("EVENT_TOPIC", "projects/rhea-459720/topics/mailman-new-email")
    PROJECT_ID = os.getenv("PROJECT_ID", "rhea-459720")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


