import pytest
from record import Record


def test_record():
    data = [
        63931.0, 0, 9.616672, 1.693681, 1.1903, 0.145102, -0.085642, 0.022828, 0.094119, 0.038592,
        -0.010581, -0.956543, 0.226807, -0.257324, 0.09617, 0.016926, 0.011892, 1.0, 0.000471,
        0.000193, -5.3e-05, 50.229801, -77.893475, -121.232079, 0, 0, 0.0, 0, 0, 0
    ]

    record = Record.from_csv_row(data)
    for name, expected_value in zip(record.column_names, data):
        assert record[name] == expected_value


def test_record_data_not_complete():
    with pytest.raises(ValueError):
        Record.from_csv_row([0.24, 0.21])
