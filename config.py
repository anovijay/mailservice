# config.py
import os

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "test")  # 'test' or 'prod'
    GCS_BUCKET = os.getenv("GCS_BUCKET", "test-bucket")
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_SERVER = os.getenv("EMAIL_SERVER", "imap.gmail.com")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT", 993))
    EVENT_TOPIC = os.getenv("EVENT_TOPIC", "projects/my-project/topics/email-events")
    PROJECT_ID = os.getenv("PROJECT_ID", "my-project")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
