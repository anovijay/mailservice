# event_notifier.py
from google.cloud import pubsub_v1
import json
from utils.helpers import log_info

class EventNotifier:
    def __init__(self, config):
        self.topic = config.EVENT_TOPIC
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = config.PROJECT_ID

    def send_event(self, uploaded_files, success=True, error=None):
        message = {
            "status": "success" if success else "failure",
            "uploaded_files": uploaded_files,
            "error": error,
        }
        data = json.dumps(message).encode("utf-8")
        topic_path = self.publisher.topic_path(self.project_id, self.topic.split("/")[-1])
        self.publisher.publish(topic_path, data=data)
        log_info(f"Event sent: {message}")
