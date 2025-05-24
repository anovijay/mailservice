from config import Config
from mailreader.email_client import EmailClient
from mailreader.parser import EmailParser
from storage.gcs_uploader import GCSUploader
from notifier.event_notifier import EventNotifier
from utils.helpers import log_info, log_error


def run_job():
    log_info(f"Starting MailService job in '{Config.ENVIRONMENT}' mode")

    email_client = EmailClient(Config)
    parser = EmailParser()
    uploader = GCSUploader(Config)
    notifier = EventNotifier(Config)

    uploaded_files = []

    try:
        messages = email_client.fetch_emails()
        for msg in messages:
            files = parser.extract_files(msg)
            print("Extracted:", [f["filename"] for f in files])
            
            if not files:
                log_info("No files found in email.")
                continue

            if Config.ENVIRONMENT == "prod":
                uploaded = uploader.upload_files(files)
                uploaded_files.extend(uploaded)
            else:
                log_info(f"[TEST MODE] Parsed files: {[f['filename'] for f in files]}")

        notifier.send_event(uploaded_files)

    except Exception as e:
        log_error(f"Exception during job: {e}")
        notifier.send_event([], success=False, error=str(e))


if __name__ == "__main__":
    run_job()
