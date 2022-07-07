
import pandas as pd
from dateutil import parser
from typing import Iterable, List
from tsfresh.feature_extraction import extract_features, MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute
from utils import kafka_producer


class SimpleProcessor:

    TOPIC_NAME = "simple_features_topic"

    fields = [
        "Timestamp", "Surface", "SensorLocation", "UserId",
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z",
        "Mag_X", "Mag_Y", "Mag_Z"
    ]

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
                elif field == "Timestamp":
                    result_record[field] = parser.parse(record[field])
                else:
                    if isinstance(record[field], str):
                        result_record[field] = record[field].strip()
                    else:
                        result_record[field] = record[field]

            data.append(result_record)

        return pd.DataFrame(data)
    
    def extract_classes(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(
            by=["UserId", "Surface"]
        ).count().reset_index()[["UserId", "Surface"]]

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        return extract_features(
            df.drop(["Surface", "SensorLocation"], axis=1),
            column_id="UserId",
            column_sort="Timestamp",
            impute_function=impute,
            default_fc_parameters=MinimalFCParameters()
        )

    def process(self, stream: Iterable[dict]) -> dict:
        df = self.stream_to_df(stream)
        classes = self.extract_classes(df)
        df_features = self.extract_features(df)

        return (df_features.to_dict(), classes.to_dict())
