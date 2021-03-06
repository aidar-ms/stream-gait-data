

import json
import core.config as config
from kafka import KafkaConsumer
from utils import kafka_consumer


class Receiver:

    SOURCE_FILE = "file"
    SOURCE_KAFKA = "kafka"

    handle = None

    stream = None

    def __init__(self, source_type: str, source_name: str) -> None:
        """
        source_type is one of: file, s3
        """
        if source_type == "file":
            self.handle = open(source_name)
            self.stream = (json.loads(m) for m in self.handle)
        elif source_type == "kafka":
            self.handle = kafka_consumer(source_name, config.KAFKA_HOST)
            self.stream = (m.value for m in self.handle)
    
    def close(self):
        self.handle.close()
