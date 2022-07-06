

from datetime import datetime
from random import choice
from typing import List

from core.streamer import Streamer
from records.surface import SurfaceRecord


class MixingGenerator:

    def __init__(self, streamer: Streamer, source_type: str, source_name: str) -> None:
        self.streamer = streamer
        self.source_type = source_type
        self.source_name = source_name

    def stream(self, user_ids: List[int]):
        user_ids = user_ids.copy()

        streams = {user_id: self.streamer.data(user_id) for user_id in user_ids}
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
