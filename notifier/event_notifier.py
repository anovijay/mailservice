from google.cloud import pubsub_v1
import json
from utils.helpers import log_info, log_error

class EventNotifier:
    def __init__(self, config):
        self.topic = config.EVENT_TOPIC
        self.project_id = config.PROJECT_ID
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            self.project_id, self.topic.split("/")[-1]
        )

    def send_event(self, uploaded_files, success=True, error=None):
        event = {
            "status": "success" if success else "failure",
            "uploaded_files": uploaded_files,
            "error": error,
        }

        try:
            data = json.dumps(event).encode("utf-8")
            future = self.publisher.publish(self.topic_path, data=data)
            message_id = future.result()
            log_info(f"[PubSub] Event published to {self.topic_path} with ID {message_id}")
            log_info(f"[PubSub] Payload: {event}")
        except Exception as e:
            log_error(f"[PubSub] Failed to publish event: {str(e)}")
            log_error(f"[PubSub] Payload was: {event}")
