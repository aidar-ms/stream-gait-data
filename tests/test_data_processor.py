import pandas as pd
from data_generators.records.surface import SurfaceRecord
from data_processors.simple_processor.processor import SimpleProcessor


def test_data_processor():
    data_record = {
        "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18880", "SampleTimeFine": " ",
        "Acc_X": " 10.124899", "Acc_Y": " 1.016880", "Acc_Z": " -4.122343", "FreeAcc_X": " 0.722358",
        "FreeAcc_Y": " 0.934328", "FreeAcc_Z": " 1.102719", "Gyr_X": " 0.134887", "Gyr_Y": " -0.655135",
        "Gyr_Z": " 0.182726", "Mag_X": " -0.839111", "Mag_Y": " -0.054199", "Mag_Z": " 0.741211",
        "VelInc_X": " 0.101374", "VelInc_Y": " 0.010289", "VelInc_Z": " -0.040885", "OriInc_q0": " 0.999994",
        "OriInc_q1": " 0.000674", "OriInc_q2": " -0.003276", "OriInc_q3": " 0.000914", "Roll": " 179.815009",
        "Pitch": " -64.272185", "Yaw": " 109.360270", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000",
        "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "
    }

    print(SurfaceRecord.from_json(data_record))


def test_record_stream_processing():
    stream = [
        {"Timestamp": "2022-05-29 13:09:15", "UserId": 1, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18880", "SampleTimeFine": " ", "Acc_X": " 10.124899", "Acc_Y": " 1.016880", "Acc_Z": " -4.122343", "FreeAcc_X": " 0.722358", "FreeAcc_Y": " 0.934328", "FreeAcc_Z": " 1.102719", "Gyr_X": " 0.134887", "Gyr_Y": " -0.655135", "Gyr_Z": " 0.182726", "Mag_X": " -0.839111", "Mag_Y": " -0.054199", "Mag_Z": " 0.741211", "VelInc_X": " 0.101374", "VelInc_Y": " 0.010289", "VelInc_Z": " -0.040885", "OriInc_q0": " 0.999994", "OriInc_q1": " 0.000674", "OriInc_q2": " -0.003276", "OriInc_q3": " 0.000914", "Roll": " 179.815009", "Pitch": " -64.272185", "Yaw": " 109.360270", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:09:18", "UserId": 1, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18881", "SampleTimeFine": " ", "Acc_X": " 10.577986", "Acc_Y": " 0.374224", "Acc_Z": " -4.749983", "FreeAcc_X": " 0.236218", "FreeAcc_Y": " 0.453230", "FreeAcc_Z": " 1.777585", "Gyr_X": " 0.179794", "Gyr_Y": " -0.646717", "Gyr_Z": " 0.186310", "Mag_X": " -0.835205", "Mag_Y": " -0.012939", "Mag_Z": " 0.739990", "VelInc_X": " 0.105929", "VelInc_Y": " 0.003883", "VelInc_Z": " -0.047154", "OriInc_q0": " 0.999994", "OriInc_q1": " 0.000899", "OriInc_q2": " -0.003234", "OriInc_q3": " 0.000932", "Roll": " -179.859957", "Pitch": " -63.898460", "Yaw": " 109.113778", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:09:20", "UserId": 1, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18882", "SampleTimeFine": " ", "Acc_X": " 10.864512", "Acc_Y": " -0.118242", "Acc_Z": " -5.088397", "FreeAcc_X": " -0.164038", "FreeAcc_Y": " 0.210183", "FreeAcc_Z": " 2.181968", "Gyr_X": " 0.335256", "Gyr_Y": " -0.607734", "Gyr_Z": " 0.192588", "Mag_X": " -0.810547", "Mag_Y": " -0.088867", "Mag_Z": " 0.753418", "VelInc_X": " 0.108800", "VelInc_Y": " -0.000993", "VelInc_Z": " -0.050555", "OriInc_q0": " 0.999994", "OriInc_q1": " 0.001676", "OriInc_q2": " -0.003039", "OriInc_q3": " 0.000963", "Roll": " -179.438930", "Pitch": " -63.519287", "Yaw": " 108.860317", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:12:02", "UserId": 2, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18883", "SampleTimeFine": " ", "Acc_X": " 10.900772", "Acc_Y": " -0.370402", "Acc_Z": " -5.602181", "FreeAcc_X": " -0.236459", "FreeAcc_Y": " -0.212870", "FreeAcc_Z": " 2.444830", "Gyr_X": " 0.477849", "Gyr_Y": " -0.525883", "Gyr_Z": " 0.181145", "Mag_X": " -0.839844", "Mag_Y": " -0.010742", "Mag_Z": " 0.752930", "VelInc_X": " 0.109158", "VelInc_Y": " -0.003472", "VelInc_Z": " -0.055743", "OriInc_q0": " 0.999993", "OriInc_q1": " 0.002389", "OriInc_q2": " -0.002629", "OriInc_q3": " 0.000906", "Roll": " -178.964681", "Pitch": " -63.213267", "Yaw": " 108.636413", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:12:03", "UserId": 2, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18884", "SampleTimeFine": " ", "Acc_X": " 10.618466", "Acc_Y": " -0.819458", "Acc_Z": " -5.583561", "FreeAcc_X": " -0.600369", "FreeAcc_Y": " -0.392372", "FreeAcc_Z": " 2.190841", "Gyr_X": " 0.529548", "Gyr_Y": " -0.451129", "Gyr_Z": " 0.171160", "Mag_X": " -0.806641", "Mag_Y": " -0.051758", "Mag_Z": " 0.756592", "VelInc_X": " 0.106317", "VelInc_Y": " -0.007956", "VelInc_Z": " -0.055617", "OriInc_q0": " 0.999994", "OriInc_q1": " 0.002648", "OriInc_q2": " -0.002256", "OriInc_q3": " 0.000856", "Roll": " -178.470370", "Pitch": " -62.922735", "Yaw": " 108.424207", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:04:10", "UserId": 3, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18885", "SampleTimeFine": " ", "Acc_X": " 10.959066", "Acc_Y": " -0.790155", "Acc_Z": " -4.500065", "FreeAcc_X": " -0.927426", "FreeAcc_Y": " 0.732867", "FreeAcc_Z": " 2.001647", "Gyr_X": " 0.566192", "Gyr_Y": " -0.427879", "Gyr_Z": " 0.170702", "Mag_X": " -0.818604", "Mag_Y": " -0.038818", "Mag_Z": " 0.762695", "VelInc_X": " 0.109693", "VelInc_Y": " -0.007681", "VelInc_Z": " -0.044788", "OriInc_q0": " 0.999993", "OriInc_q1": " 0.002831", "OriInc_q2": " -0.002139", "OriInc_q3": " 0.000854", "Roll": " -177.968833", "Pitch": " -62.671294", "Yaw": " 108.225405", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "},
        {"Timestamp": "2022-05-29 13:04:11", "UserId": 3, "Surface": "StrU", "SensorLocation": "Left shank", "PacketCounter": "18886", "SampleTimeFine": " ", "Acc_X": " 11.863618", "Acc_Y": " -0.419583", "Acc_Z": " -3.446319", "FreeAcc_X": " -1.015301", "FreeAcc_Y": " 2.195329", "FreeAcc_Z": " 2.309523", "Gyr_X": " 0.454743", "Gyr_Y": " -0.391696", "Gyr_Z": " 0.195887", "Mag_X": " -0.819336", "Mag_Y": " 0.006836", "Mag_Z": " 0.760986", "VelInc_X": " 0.118707", "VelInc_Y": " -0.004002", "VelInc_Z": " -0.034240", "OriInc_q0": " 0.999995", "OriInc_q1": " 0.002274", "OriInc_q2": " -0.001958", "OriInc_q3": " 0.000979", "Roll": " -177.499935", "Pitch": " -62.413313", "Yaw": " 107.992820", "Latitude": " ", "Longitude": " ", "Altitude": " 0.000000", "Vel_X": " ", "Vel_Y": " ", "Vel_Z": " "}
    ]

    sp = SimpleProcessor()
    res: pd.DataFrame = sp.stream_to_df(stream)

    assert len(res.columns) == len(SimpleProcessor.fields)
    assert len(res) == len(stream)

    # Extract features
    df_features = sp.extract_features(res)
    assert len(df_features) == 3
