from argparse import ArgumentParser
from core.receiver import Receiver
from core.emitter import Emitter
from processor import SimpleProcessor


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("-st", "--source-type", dest="source_type", help="Receiver source type (Kafka or a file)")
    parser.add_argument("-sn", "--source-name", dest="source_name", help="Receiver source name (topic or file name)")
    parser.add_argument("-dt", "--dest-type", dest="dest_type", help="Destination type (Kafka or a file)")
    parser.add_argument("-dn", "--dest-name", dest="dest_name", help="Destination name (topic or file name)")
    parser.add_argument("-l", "--record-limit", dest="limit", type=int, default=250, help="How many records should be flushed to a destination at a time")

    args = parser.parse_args()

    source_type = args.source_type
    source_name = args.source_name
    dest_type = args.dest_type
    dest_name = args.dest_name
    limit = args.limit

    sp = SimpleProcessor()
    r = Receiver(source_type, source_name)
    e = Emitter(dest_type, dest_name)

    try:
        data = []
        for record in r.stream:
            data.append(record)
            if len(data) >= limit:
                features, classes = sp.process(data)
                payload = {
                    "features": features,
                    "classes": classes
                }
                e.send(payload)
                data.clear()
    except KeyboardInterrupt:
        r.close()
        e.close()
