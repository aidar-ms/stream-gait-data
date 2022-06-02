import pytest
from records.surface import SurfaceRecord, TrainingSurfaceRecord


def test_record():
    data = [
        63931.0, 0, 9.616672, 1.693681, 1.1903, 0.145102, -0.085642, 0.022828, 0.094119, 0.038592,
        -0.010581, -0.956543, 0.226807, -0.257324, 0.09617, 0.016926, 0.011892, 1.0, 0.000471,
        0.000193, -5.3e-05, 50.229801, -77.893475, -121.232079, 0, 0, 0.0, 0, 0, 0
    ]

    record = SurfaceRecord.from_csv_row(data)
    for name, expected_value in zip(record.column_names, data):
        assert record[name] == expected_value


def test_training_record():
    data = [
        2, "95", 63931.0, 0, 9.616672, 1.693681, 1.1903, 0.145102, -0.085642, 0.022828, 0.094119, 0.038592,
        -0.010581, -0.956543, 0.226807, -0.257324, 0.09617, 0.016926, 0.011892, 1.0, 0.000471,
        0.000193, -5.3e-05, 50.229801, -77.893475, -121.232079, 0, 0, 0.0, 0, 0, 0
    ]

    record = TrainingSurfaceRecord.from_csv_row(data)
    for name, expected_value in zip(record.column_names, data):
        if name == "Surface":
            assert record[name] == TrainingSurfaceRecord.get_surface(expected_value)
        elif name == "SensorLoc":
            assert record[name] == TrainingSurfaceRecord.get_sensor_location(expected_value)
        else:
            assert record[name] == expected_value

@pytest.mark.parametrize(
    "surface_code, surface",
    (
        (2, "CALIB"), (6, "FE"), (9, "FE"), (10, "CS"),
        (28, "SlpU"), (35, "SlpD"), (50, "BnkL"), (43, "BnkR"),
        (55, "GR"), (100, None)
    )
)
def test_training_record_get_surface(surface_code, surface):
    assert TrainingSurfaceRecord.get_surface(surface_code) == surface

def test_record_data_not_complete():
    with pytest.raises(ValueError):
        SurfaceRecord.from_csv_row([0.24, 0.21])
