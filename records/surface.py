from collections import UserDict
from datetime import datetime
from typing import List, Union


class SurfaceRecord(UserDict):

    column_names = [
        'PacketCounter',
        'SampleTimeFine',
        'Acc_X',
        'Acc_Y',
        'Acc_Z',
        'FreeAcc_X',
        'FreeAcc_Y',
        'FreeAcc_Z',
        'Gyr_X',
        'Gyr_Y',
        'Gyr_Z',
        'Mag_X',
        'Mag_Y',
        'Mag_Z',
        'VelInc_X',
        'VelInc_Y',
        'VelInc_Z',
        'OriInc_q0',
        'OriInc_q1',
        'OriInc_q2',
        'OriInc_q3',
        'Roll',
        'Pitch',
        'Yaw',
        'Latitude',
        'Longitude',
        'Altitude',
        'Vel_X',
        'Vel_Y',
        'Vel_Z'
    ]

    @classmethod
    def from_csv_row(cls, user_id: int, data: List[float]):
        if len(data) != len(cls.column_names):
            raise ValueError(f"Length of data list does not match the length of column names list: {len(data)} != {len(cls.column_names)}")

        record = cls()
        record["UserId"] = user_id
        record["Timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for name, value in zip(cls.column_names, data):
            record[name] = value

        return record
    
    @classmethod
    def from_json(cls, data: dict):
        # if len(data) != len(cls.column_names):
        #     raise ValueError(f"Length of data list does not match the length of column names list: {len(data)} != {len(cls.column_names)}")
        
        numeric_field_names = {
            "PacketCounter", "Acc_X", "Acc_Y", "Acc_Z", "FreeAcc_X", "FreeAcc_Y", "FreeAcc_Z",
            "Gyr_X", "Gyr_Y", "Gyr_Z", "Mag_X", "Mag_Y", "Mag_Z", "VelInc_X", "VelInc_Y", "VelInc_Z",
            "OriInc_q0", "OriInc_q1", "OriInc_q2", "OriInc_q3",
            "Roll", "Pitch", "Yaw", "Altitude"
        }

        record = cls()
        for name in cls.column_names:
            if name in numeric_field_names:
                record[name] = float(data[name].strip())  # TODO: Try double too
            else:
                record[name] = data[name].strip()

        return record




class TrainingSurfaceRecord(SurfaceRecord):

    column_names = ["Surface", "SensorLoc"] + SurfaceRecord.column_names

    SURFACE_MAP = {
        (1, 2, 3): "CALIB",
        (4, 5, 6, 7, 8, 9): "FE",
        (10, 11, 12, 13, 14, 15): "CS",
        (16, 18, 20, 22, 24, 26): "StrU",
        (17, 19, 21, 23, 25, 27): "StrD",
        (28, 30, 32, 34, 36, 38): "SlpU",
        (29, 31, 33, 35, 37, 39): "SlpD",
        (40, 42, 44, 46, 48, 50): "BnkL",
        (41, 43, 45, 47, 49, 51): "BnkR",
        (52, 53, 54, 55, 56, 57): "GR",
    }

    SENSOR_LOC_MAP = {
        "CC": "Trunk",
        "95": "Wrist",
        "93": "Right thigh",
        "8B": "Left thigh",
        "9B": "Right shank",
        "B6": "Left shank"
    }

    def __setitem__(self, key, item) -> None:
        if key == "Surface":
            item = self.get_surface(item)
        elif key == "SensorLoc":
            item = self.get_sensor_location(item)

        return super().__setitem__(key, item)

    @classmethod
    def get_surface(cls, surface_code: Union[int, str]) -> str:
        if isinstance(surface_code, str):
            surface_code = int(surface_code)

        for bucket in cls.SURFACE_MAP:
            # NOTE: Linear search will do just fine...
            if binary_search_bucket(surface_code, bucket) is not None:
                return cls.SURFACE_MAP[bucket]
    
    @classmethod
    def get_sensor_location(cls, sensor_location_code: str) -> str:
        return cls.SENSOR_LOC_MAP.get(sensor_location_code)


def binary_search_bucket(n, bucket):
    l, r = 0, len(bucket) - 1
    while l <= r:
        m = l + (r - l) // 2
        if n < bucket[m]:
            r = m - 1
        elif n > bucket[m]:
            l = m + 1
        else:
            return bucket[m]
