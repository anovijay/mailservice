# main.py
from config import Config
from email.email_client import EmailClient
from email.parser import EmailParser
from storage.gcs_uploader import GCSUploader
from notifier.event_notifier import EventNotifier
from utils.helpers import log_info, log_error

def run_job():
    log_info("Starting Email to GCS Job")
    
    email_client = EmailClient(Config)
    parser = EmailParser()
    uploader = GCSUploader(Config)
    notifier = EventNotifier(Config)

    uploaded_files = []
    
    try:
        messages = email_client.fetch_emails()
        for msg in messages:
            files = parser.extract_files(msg)
            if Config.ENVIRONMENT == "prod":
                uploaded = uploader.upload_files(files)
                uploaded_files.extend(uploaded)
            else:
                log_info(f"Skipping upload in {Config.ENVIRONMENT} mode. Parsed files: {files}")

        notifier.send_event(uploaded_files)

    except Exception as e:
        log_error(f"Error running job: {str(e)}")
        notifier.send_event([], success=False, error=str(e))

if __name__ == "__main__":
    run_job()
