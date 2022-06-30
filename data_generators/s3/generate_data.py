"""
Generates data from S3 objects. Each object is a csv file with user id as a file name, e.g. 1.csv, 2.csv, ...
"""
from datetime import datetime
import boto3
from argparse import ArgumentParser
from random import choice
from typing import List

from utils import kafka_producer


def stream_from_s3(user_id: int, bucket_name: str):
    s3 = boto3.resource("s3")
    s3_object = s3.Object(bucket_name, f"{user_id}.csv").get()

    for record in s3_object["Body"]:
        record = record.decode("ascii").split("\r\n")
        for row in record:
            yield row.split(",")


def generate_data(user_ids: List[int], bucket_name: str):
    data = None
    streams = {user_id: stream_from_s3(user_id, bucket_name) for user_id in user_ids}
    while len(streams) > 0:
        current_user_id = choice(user_ids)
        current_stream = streams[current_user_id]

        try:
            record = next(current_stream)
            if data is None:
                # Initialise data dictionary if None and update record variable to an actual data row
                data = {k: None for k in record}
                record = next(current_stream)

            # Python 3 dictionaries always maintain the order of keys as they were inserted,
            # so this zip iteration is safe and should ensure proper mapping between keys and values.
            for key, val in zip(data.keys(), record):
                data[key] = val
            
            data["Timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            yield data

        except StopIteration:
            del streams[current_user_id]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-kh", "--kafka-host", dest="kafka_host", default="localhost:9092")
    parser.add_argument("-d", "--bucket_name", dest="bucket_name", default="stream-gait-data-disser")
    parser.add_argument("-t", "--dest_topic", dest="dest_topic", default="training_topic")
    parser.add_argument("-ui", "--user_ids", dest="user_ids", help="Comma-separated user ids")

    args = parser.parse_args()

    if args.user_ids is None:
        raise ValueError("You need to provide a list of user ids")

    user_ids = list(map(int, args.user_ids.split(",")))
    if len(user_ids) > 5:
        # NOTE: temporary measure
        raise ValueError("Reduce the number of user ids to lte 5")

    kafka_host = args.kafka_host
    dest_topic = args.dest_topic
    bucket_name = args.bucket_name

    producer = kafka_producer(kafka_host)

    for record in generate_data(user_ids, bucket_name):
        producer.send(dest_topic, record)



