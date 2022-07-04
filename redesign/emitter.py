
import json

import config

from utils import kafka_consumer


class Emitter:

    DEST_FILE = "file"
    DEST_KAFKA = "kafka"

    def __init__(self, dest_type: str, dest_name: str) -> None:
        self.type = dest_type

        self.data = []

        if dest_type == "file":
            self.handle = open(dest_name, "w")
        elif dest_type == "kafka":
            pass
            # self.handle = kafka_consumer(dest_name, config.KAFKA_HOST)

    def send(self, msg: dict):
        if self.type == self.DEST_FILE:
            self.handle.write(json.dumps(msg) + "\n")
        

    def close(self):
        self.handle.close()