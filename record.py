from collections import UserDict
from typing import List


class Record(UserDict):

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
    def from_csv_row(cls, data: List[float]):
        if len(data) != len(cls.column_names):
            raise ValueError(f"Length of data list does not match the length of column names list: {len(data)} != {len(cls.column_names)}")

        record = cls()
        for name, value in zip(cls.column_names, data):
            record[name] = value

        return record