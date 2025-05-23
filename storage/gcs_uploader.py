# gcs_uploader.py
from google.cloud import storage
import os
from utils.helpers import log_info

class GCSUploader:
    def __init__(self, config):
        self.bucket_name = config.GCS_BUCKET
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_files(self, files):
        uploaded = []
        for file in files:
            blob = self.bucket.blob(os.path.basename(file["path"]))
            blob.upload_from_filename(file["path"])
            uploaded.append({
                "gcs_uri": f"gs://{self.bucket_name}/{blob.name}",
                "filename": file["filename"]
            })
            log_info(f"Uploaded: {file['filename']}")
        return uploaded
