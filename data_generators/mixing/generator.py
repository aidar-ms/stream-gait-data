

from datetime import datetime
from random import choice
from typing import List

from core.streamer import Streamer
from core.csv_row import CSVRow


class MixingGenerator:

    def __init__(self, streamer: Streamer) -> None:
        self.streamer = streamer

    def get_streams(self, surface_conf: dict, sensor_loc: int):
        streams = {}
        for surface_id in surface_conf:
            for user_id in surface_conf[surface_id]:
                streams[(int(surface_id), user_id)] = self.streamer.data(user_id, int(surface_id), sensor_loc)
        
        return streams

    def stream(self, surface_conf: dict, sensor_location: int):
        streams = self.get_streams(surface_conf, sensor_location)
        data = {k: None for k in CSVRow.column_names}
        # keys: (user_id, surface)
        # A key is selected randomly at each stream iteration to introduce randomness in the streamed data
        keys = list(streams.keys())

        while len(streams) > 0:
            current_key = choice(keys)
            current_stream = streams[current_key]

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
                del streams[current_key]
                keys.remove(current_key)
