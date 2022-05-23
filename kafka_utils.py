

import json
from kafka import KafkaProducer


def get_kafka_producer(server: str) -> KafkaProducer:
    return KafkaProducer(
        bootstrap_servers=server,
        value_serializer=lambda m: json.dumps(m).encode("ascii")
    )
