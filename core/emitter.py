
import json

import core.config as config

from utils import kafka_consumer, kafka_producer


class Emitter:

    # Handle must point to the storage object
    handle = None
    DEST_FILE = "file"
    DEST_KAFKA = "kafka"

    def __init__(self, dest_type: str, dest_name: str) -> None:
        self.type = dest_type

        self.dest_name = dest_name

        self.data = []

        if self.is_file:
            self.handle = open(dest_name, "w")
        elif self.is_kafka:
            self.handle = kafka_producer(config.KAFKA_HOST)

    def send(self, msg: dict):
        if self.is_file:
            self.handle.write(json.dumps(msg) + "\n")
        elif self.is_kafka:
            self.handle.send(self.dest_name, msg)

    def close(self):
        self.handle.close()
    
    @property
    def is_file(self):
        return self.type == self.DEST_FILE

    @property
    def is_kafka(self):
        return self.type == self.DEST_KAFKA