"""
Generates data from S3 objects. Each object is a csv file with user id as a file name, e.g. 1.csv, 2.csv, ...
"""
import csv
from datetime import datetime
import boto3
from argparse import ArgumentParser
from random import choice
from typing import List

from utils import kafka_producer
from records.surface import SurfaceRecord


def stream_from_file(user_id: int):

    with open(f"labeled_data/{user_id}.csv") as f:
        reader = csv.reader(f, delimiter=",")
        for line in reader:
            yield line


def stream_from_s3(user_id: int, bucket_name: str):
    s3 = boto3.resource("s3")
    s3_object = s3.Object(bucket_name, f"{user_id}.csv").get()

    prev_record = b''
    newline_char = b'\n'

    for record in s3_object["Body"]:
        if record == b'':
            break

        line = prev_record + record
        first_nl = line.find(newline_char)
        yield line.decode("ascii").rstrip()[:first_nl].split(",")
        prev_record = line[first_nl + 1:]


def get_stream(user_id: int, kind: str):

    if kind == "file":
        return stream_from_file(user_id)
    elif kind == "s3":
        # TODO move bucket name to configs
        bucket = "stream-gait-data-disser"
        return stream_from_s3(user_id, bucket)


def generate_data(user_ids: List[int], source: str):
    # TODO: Rewrite
    data = None

    streams = {user_id: get_stream(user_id, source) for user_id in user_ids}
    data = {k: None for k in SurfaceRecord.column_names}

    while len(streams) > 0:
        current_user_id = choice(user_ids)
        current_stream = streams[current_user_id]

        try:
            record = next(current_stream)
            if record[0] == "UserId" or record[5] == '':
                continue

            # Python 3 dictionaries always maintain the order of keys as they were inserted,
            # so this zip iteration is safe and should ensure proper mapping between keys and values.
            for key, val in zip(data.keys(), record):
                data[key] = val

            data["Timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            yield data

        except StopIteration:
            del streams[current_user_id]
            user_ids.remove(current_user_id)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-kh", "--kafka-host", dest="kafka_host", default="localhost:9092")
    parser.add_argument("-t", "--dest_topic", dest="dest_topic", default="training_topic")
    parser.add_argument("-ui", "--user_ids", dest="user_ids", help="Comma-separated user ids")

    parser.add_argument("-s", "--source", dest="source", default="s3")

    args = parser.parse_args()

    if args.user_ids is None:
        raise ValueError("You need to provide a list of user ids")

    user_ids = list(map(int, args.user_ids.split(",")))
    if len(user_ids) > 5:
        # NOTE: temporary measure
        raise ValueError("Reduce the number of user ids to lte 5")

    kafka_host = args.kafka_host
    dest_topic = args.dest_topic
    source = args.source

    producer = kafka_producer(kafka_host)

    for record in generate_data(user_ids, source):
        producer.send(dest_topic, record)
