import json
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import NoBrokersAvailable


def kafka_producer(kafka_host: str):
    i = 0

    while i < 4:
        try:
            producer = KafkaProducer(
                bootstrap_servers=kafka_host,
                value_serializer=lambda m: json.dumps(m).encode("ascii")
            )
            return producer
        except NoBrokersAvailable:
            # Try again after a pause
            # The sleep is needed because the broker might not get started instantly
            print("Sleeping for 10 secs")
            sleep(10)
            i += 1

    raise ValueError(f"Failed to connect after {i} tries")


def kafka_consumer(topic_name: str, kafka_host: str):
    i = 0

    while i < 4:
        try:
            return KafkaConsumer(
                topic_name,
                bootstrap_servers=[kafka_host],
                value_deserializer=lambda m: json.loads(m.decode("ascii")),
                auto_offset_reset="earliest"
            )
        except NoBrokersAvailable:
            # Try again after a pause
            # The sleep is needed because the broker might not get started instantly
            print("Sleeping for 10 secs")
            sleep(10)
            i += 1

    raise ValueError(f"Failed to connect after {i} tries")