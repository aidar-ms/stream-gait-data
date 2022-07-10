from core.records.surface import Surface
from core.records.sensor_location import SensorLocation


def test_surface():

    code = Surface.get_code(12)
    assert code == Surface.CS

    code = Surface.get_code("12")
    assert code == Surface.CS


def test_sensor_location():

    code = SensorLocation.get_code("8B")
    assert code == SensorLocation.LEFT_THIGH

    code = SensorLocation.get_code("B6")
    assert code == SensorLocation.LEFT_SHANK
