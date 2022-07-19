"""
Generates data from S3 objects. Each object is a csv file with user id as a file name, e.g. 1.csv, 2.csv, ...
"""
import json

from argparse import ArgumentParser
from time import sleep
from core.streamer import get_streamer
from data_generators.mixing.generator import MixingGenerator
from core.emitter import Emitter



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-st", "--source-type", dest="source_type", help="Receiver source type (S3 or a file)")
    parser.add_argument("-sn", "--source-name", dest="source_name", help="Receiver source name (S3 bucket name or file name)")
    parser.add_argument("-dt", "--dest-type", dest="dest_type", help="Destination type (Kafka or a file)")
    parser.add_argument("-dn", "--dest-name", dest="dest_name", help="Destination name (topic or file name)")

    parser.add_argument("-c", "--config", dest="config", help="Experiment config path")
    parser.add_argument("-pt", "--pipeline-type", dest="pipeline_type", help="Pipeline type")

    parser.add_argument("-f", "--frequency", default=100, dest="frequency", help="How many records to emit at once")
    parser.add_argument("-s", "--sleeptime", default=0.1, dest="sleeptime", help="For how many records to sleep after emitting a certain amount of data")

    args = parser.parse_args()

    # Load experiment configurations
    if args.config is None:
        raise ValueError("You need to provide a path for experiment configuration")
    
    if args.pipeline_type not in ("train", "test"):
        raise ValueError("Wrong pipeline type: " + args.pipeline_type)

    with open(args.config) as f:
        config = json.load(f)
    
    # Write CLI args to variables
    pipeline_type = args.pipeline_type
    source_type = args.source_type
    source_name = args.source_name
    dest_type = args.dest_type
    dest_name = args.dest_name
    sleeptime = args.sleeptime

    gen = MixingGenerator(get_streamer(source_name, source_type))
    emitter = Emitter(dest_type, dest_name)

    try:
        count = 0
        for record in gen.stream(config[pipeline_type], config["sensor_location"]):
            if count >= args.frequency:
                sleep(sleeptime)
                count = 0

            emitter.send(record)
            count += 1
    except KeyboardInterrupt:
        emitter.close()
