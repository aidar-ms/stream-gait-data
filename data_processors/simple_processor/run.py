from processor import SimpleProcessor
from utils import kafka_consumer

if __name__ == "__main__":
    sp = SimpleProcessor()
    kafka_host = "broker:9092"

    consumer = kafka_consumer("training_topic", kafka_host)

    data = []
    for message in consumer:
        data.append(message.value)

        if len(data) >= 1000:
            sp.process(data, kafka_host)
            print(f"Sent {len(data)} processed features to {sp.TOPIC_NAME} topic")
            data.clear()