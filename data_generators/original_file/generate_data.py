"""
Script that supplies data based on dataset from the paper: "A database of human gait performance on irregular and uneven surfaces collected by wearable sensors"
URL link: https://www.nature.com/articles/s41597-020-0563-y

Generates data based on a csv directory in the file system, as downloaded from the original source

"""
import csv
import os

import re

from argparse import ArgumentParser
from time import sleep
from multiprocessing import Pool
from time import sleep
from records.surface import TrainingSurfaceRecord
from utils import kafka_producer


def publish_participant_data(participant: int, topic_name: str, kafka_host: str, frequency: str, data_root: str):
    participant_data_path = os.path.join(data_root, str(participant))
    if not os.path.isdir(participant_data_path):
        raise ValueError(f"Invalid participant path: {participant_data_path}")

    producer = kafka_producer(kafka_host)

    print(f"Emitting data for participant: {participant}")
    total_count = 0
    try:
        file_format_match = re.compile(r"^(\d{1,2})\-000_00B432([\w]{2})\.txt\.csv$")
        for contents in os.walk(participant_data_path):
            for fname in contents[2]:
                match = file_format_match.match(fname)
                if match is None:
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

                        # Walking surface and sensor location are encoded in the file name
                        line = [match.group(1), match.group(2)] + line
                        producer.send(topic_name, TrainingSurfaceRecord.from_csv_row(participant, line).data)
                        total_count += 1
                        tmp_counter += 1
    except Exception as e:
        print(f"Exiting due to an exception: {str(e)}")
    except KeyboardInterrupt:
        print(f"Exiting due to a keyboard interrupt")
    finally:
        producer.close()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-kh", "--kafka-host", dest="kafka_host", default="localhost:9092")
    parser.add_argument("-d", "--data-dir", dest="data_dir", default="input_data_SD")
    parser.add_argument("-t", "--topic_name", dest="topic_name", default="training_topic")
    parser.add_argument("-ui", "--user_ids", dest="user_ids", help="Comma-separated user ids")
    parser.add_argument("-fq", "--frequency", dest="frequency", default=60)

    args = parser.parse_args()

    if args.user_ids is None:
        raise ValueError("You need to provide a list of participant numbers")

    user_ids = list(map(int, args.user_ids.split(",")))
    if len(user_ids) > 5:
        # NOTE: temporary measure
        raise ValueError("Reduce the number of user ids to lte 5")

    frequency = args.frequency
    kafka_host = args.kafka_host
    topic_name = args.topic_name

    data_dir = args.data_dir
    data_root = data_dir

    pool = Pool(len(user_ids))
    params = [(p, topic_name, kafka_host, frequency, data_root) for p in user_ids]
    try:
        pool.starmap(publish_participant_data, ((p, topic_name, kafka_host, frequency, data_root) for p in user_ids))
    except KeyboardInterrupt:
        print("Exiting")
        pool.close()