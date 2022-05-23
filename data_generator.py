
import csv
import os

import re

from argparse import ArgumentParser
from time import sleep, time

from kafka_utils import get_kafka_producer
from record import Record


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-kh", "--kafka-host", dest="kafka_host", default="localhost:9092")
    parser.add_argument("-d", "--data-dir", dest="data_dir", default="input_data_SD")
    parser.add_argument("-p", "--participant", dest="participant")
    parser.add_argument("-fq", "--frequency", dest="frequency", default=60)

    args = parser.parse_args()

    data_dir = args.data_dir
    participant = args.participant
    frequency = args.frequency
    kafka_host = args.kafka_host

    data_root = os.path.join(os.path.dirname(__file__), data_dir)
    participant_data_path = os.path.join(data_root, participant)
    if not os.path.isdir(participant_data_path):
        raise ValueError(f"Invalid participant number: {participant}")

    producer = get_kafka_producer(server=kafka_host)
    topic_name = f"participant_{participant}"

    print(f"Emitting data for participant: {participant}")
    total_count = 0
    try:
        file_format_match = re.compile(r".+\.txt\.csv")
        for contents in os.walk(participant_data_path):
            for fname in contents[2]:
                if not file_format_match.match(fname):
                    continue

                with open(os.path.join(participant_data_path, fname)) as f:
                    tmp_counter = 0
                    data = csv.reader(f)
                    for line in data:
                        if len(line) == 0:
                            print("Skipping an empty line")
                            continue

                        if line[0] == "PacketCounter":
                            continue

                        # Sleep after emitting every N records to imitate frequency
                        if tmp_counter == frequency:
                            tmp_counter = 0
                            print(f"Emitted {frequency} records. Total emitted count: {total_count}")
                            sleep(1)
                        
                        producer.send(topic_name, Record.from_csv_row(line).data)
                        total_count += 1
                        tmp_counter += 1

    except KeyboardInterrupt as ke:
        print("\nExiting...")
    finally:
        producer.close()

