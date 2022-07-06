"""
Generates data from S3 objects. Each object is a csv file with user id as a file name, e.g. 1.csv, 2.csv, ...
"""
import os

from argparse import ArgumentParser
from core.streamer import get_streamer
from data_generators.mixing.generator import MixingGenerator
from core.emitter import Emitter



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-st", "--source-type", dest="source_type", help="Receiver source type (S3 or a file)")
    parser.add_argument("-sn", "--source-name", dest="source_name", help="Receiver source name (S3 bucket name or file name)")
    parser.add_argument("-dt", "--dest-type", dest="dest_type", help="Destination type (Kafka or a file)")
    parser.add_argument("-dn", "--dest-name", dest="dest_name", help="Destination name (topic or file name)")

    parser.add_argument("-ui", "--user_ids", dest="user_ids", help="Comma-separated user ids")

    args = parser.parse_args()
    if args.user_ids is None:
        raise ValueError("You need to provide a list of user ids")
    user_ids = list(map(int, args.user_ids.split(",")))
    if len(user_ids) > 5:
        # NOTE: temporary measure
        raise ValueError("Reduce the number of user ids to lte 5")

    source_type = args.source_type
    source_name = args.source_name
    dest_type = args.dest_type
    dest_name = args.dest_name

    streamer = get_streamer(source_name, source_type)

    gen = MixingGenerator(streamer, source_type, source_name)
    emitter = Emitter(dest_type, dest_name)

    for record in gen.stream(user_ids):
        emitter.send(record)
