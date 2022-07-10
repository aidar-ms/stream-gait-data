import os
import csv
import boto3


class Streamer:

    SURFACE_COLUMN_IDX = 1

    def __init__(self, source: str) -> None:
        self.source = source

    def data(self, user_id: int, surface: int, sensor_loc: int):
        raise NotImplementedError


class FileStreamer(Streamer):

    def data(self, user_id: int, surface: int, sensor_loc: int):
        full_path = os.path.join(self.source, f"{user_id}_{surface}_{sensor_loc}.csv")

        with open(full_path) as f:
            reader = csv.reader(f, delimiter=",")
            for line in reader:
                yield line


class S3Streamer(Streamer):

    def __init__(self, source: str) -> None:
        super().__init__(source)


    def data(self, user_id: int, surface: int, sensor_loc: int):
        s3 = boto3.resource("s3")
        folder = "labeled_data"
        prev_record = b''
        newline_char = b'\n'

        key = f"{folder}/{user_id}_{surface}_{sensor_loc}.csv"
        s3_object = s3.Object(self.source, key).get()
        stream = s3_object["Body"]

        for record in stream:
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
