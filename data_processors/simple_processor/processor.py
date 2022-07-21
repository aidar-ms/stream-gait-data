
import pandas as pd
from dateutil import parser
from typing import Iterable
from scipy import signal
from sklearn.preprocessing import MinMaxScaler
from tsfresh.feature_extraction import extract_features, MinimalFCParameters
from tsfresh.utilities.dataframe_functions import impute


class SimpleProcessor:

    TOPIC_NAME = "simple_features_topic"

    def __init__(self) -> None:
        self.filter = signal.butter(2, 6, btype="lp", fs=100, output="sos")

    fields = [
        "PacketCounter", "Surface", "SensorLocation", "UserId",
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z",
        "Mag_X", "Mag_Y", "Mag_Z"
    ]

    numeric_fields = {
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z",
        "Mag_X", "Mag_Y", "Mag_Z"
    }

    butterworth_columns = {
        "Acc_X", "Acc_Y", "Acc_Z",
        "Gyr_X", "Gyr_Y", "Gyr_Z"
    }

    def stream_to_df(self, stream: Iterable[dict]):
        data = []
        for record in stream:
            result_record = {}
            for field in self.fields:
                if field in self.numeric_fields:
                    result_record[field] = float(record[field].strip())
                elif field == "PacketCounter":
                    result_record[field] = int(record[field])
                else:
                    if isinstance(record[field], str):
                        result_record[field] = record[field].strip()
                    else:
                        result_record[field] = record[field]
    
            data.append(result_record)

        df = pd.DataFrame(data)

        # Apply Butterworth filter to each user id group in the current window
        df.sort_values(["UserId", "PacketCounter"], inplace=True, ignore_index=True)
        user_ids = df.UserId.unique()
        for user_id in user_ids:
            for column in self.butterworth_columns:
                df.loc[df["UserId"] == user_id, [column]] = signal.sosfilt(self.filter, df[df["UserId"] == user_id][column])

        return df
    
    def extract_classes(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.groupby(
            by=["UserId", "Surface"]
        ).count().reset_index()[["UserId", "Surface"]]

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        def should_be_dropped(c: str):
            return (
                c.endswith("sum_values") or c.endswith("length")
            )
        
        # Extract features
        features = extract_features(
            df.drop(["Surface", "SensorLocation"], axis=1),
            column_id="UserId",
            column_sort="PacketCounter",
            impute_function=impute,
            default_fc_parameters=MinimalFCParameters()
        )

        # Drop unneeded features
        features = features[[c for c in features.columns if not should_be_dropped(c)]]

        # Scale features
        for c in features.columns:
            features[c] = MinMaxScaler().fit_transform(features[[c]])
        
        return features

    def process(self, stream: Iterable[dict]) -> dict:
        df = self.stream_to_df(stream)
        classes = self.extract_classes(df)
        df_features = self.extract_features(df)

        return (df_features.to_dict(), classes.to_dict())
