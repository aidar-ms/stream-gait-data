import os
import csv
import boto3


class Streamer:

    def __init__(self, source: str) -> None:
        self.source = source

    def data(self, user_id: int):
        raise NotImplementedError


class FileStreamer(Streamer):

    def data(self, user_id: int):
        full_path = os.path.join(self.source_dir, f"{user_id}.csv")

        with open(full_path) as f:
            reader = csv.reader(f, delimiter=",")
            for line in reader:
                yield line


class S3Streamer(Streamer):

    def __init__(self, source: str) -> None:
        super().__init__(source)


    def data(self, user_id: int):
        s3 = boto3.resource("s3")
        s3_object = s3.Object(self.source, f"{user_id}.csv").get()

        prev_record = b''
        newline_char = b'\n'

        for record in s3_object["Body"]:
            if record == b'':
                break

            line = prev_record + record
            first_nl = line.find(newline_char)
            yield line.decode("ascii").rstrip()[:first_nl].split(",")
            prev_record = line[first_nl + 1:]


def get_streamer(source: str, kind: str):
    if kind == "file":
        return FileStreamer(source)
    elif kind == "s3":
        return S3Streamer(source)
