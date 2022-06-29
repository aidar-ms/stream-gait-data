
import pandas as pd
from dateutil import parser
from typing import Iterable, List
from tsfresh.feature_extraction import extract_features, MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute
from utils import kafka_producer


class SimpleProcessor:

    TOPIC_NAME = "simple_features_topic"

    fields = [
        "Timestamp", "Surface", "SensorLoc", "UserId",
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z",
        "Mag_X", "Mag_Y", "Mag_Z"
    ]

    surfaces = {
        "CALIB": 1,
        "FE": 2,
        "CS": 3,
        "StrU": 4,
        "StrD": 5,
        "SlpU": 6,
        "SlpD": 7,
        "BnkL": 8,
        "BnkR": 9,
        "GR": 10,
    }

    sensor_locations = {
        "Trunk": 1,
        "Wrist": 2,
        "Right thigh": 3,
        "Left thigh": 4,
        "Right shank": 5,
        "Left shank": 6
    }

    numeric_fields = {
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z",
        "Mag_X", "Mag_Y", "Mag_Z"
    }

    def stream_to_df(self, stream: Iterable[dict]):
        data = []
        for record in stream:
            result_record = {}
            for field in self.fields:
                if field in self.numeric_fields:
                    result_record[field] = float(record[field].strip())
                elif field == "Surface":
                    result_record[field] = self.surfaces[record[field]]
                elif field == "SensorLoc":
                    result_record[field] = self.sensor_locations[record[field]]
                elif field == "Timestamp":
                    result_record[field] = parser.parse(record[field])
                else:
                    if isinstance(record[field], str):
                        result_record[field] = record[field].strip()
                    else:
                        result_record[field] = record[field]

            data.append(result_record)

        return pd.DataFrame(data)
    

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return extract_features(
            df.drop(["Surface", "SensorLoc"], axis=1),
            column_id="UserId",
            column_sort="Timestamp",
            impute_function=impute,
            default_fc_parameters=MinimalFCParameters()
        )
    

    def process(self, stream: Iterable[dict], kafka_host: str) -> List[dict]:
        producer = kafka_producer(kafka_host)
        df = self.stream_to_df(stream)
        df_features = self.extract_features(df)

        for record in df_features.to_dict().values():
            producer.send(self.TOPIC_NAME, record)
