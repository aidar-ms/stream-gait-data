from argparse import ArgumentParser
import json
from kafka import KafkaConsumer, TopicPartition


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--partition", dest="partition", help="Partition number")

    args = parser.parse_args()
    partition = args.partition
    consumer = KafkaConsumer(bootstrap_servers=["localhost:9092"], value_deserializer=lambda m: json.loads(m.decode("ascii")))
    if "training_topic" not in consumer.topics():
        raise ValueError
    
    consumer.assign([TopicPartition("training_topic", int(partition))])
    # consumer.subscribe("training_topic")

    try:
        for m in consumer:
            print(m.partition, m.offset, m.key.decode("ascii"), m.value["Acc_X"].strip())
    except KeyboardInterrupt:
        print("Exiting")
