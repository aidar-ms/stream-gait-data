from core.records.surface import Surface
from core.records.sensor_location import SensorLocation


class CSVRow:

    column_names = [
        'UserId',
        'Surface',
        'SensorLocation',
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
        'Yaw'
    ]

    @classmethod
    def row(cls, user_id, surface_code, sensor_location_code, row):
        return [
            user_id,
            Surface.get_code(surface_code),
            SensorLocation.get_code(sensor_location_code)
        ] + list(map(str.strip, row[:len(row) - 6]))  # last 6 columns in the original file are meaningless
