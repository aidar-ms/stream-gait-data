import json
from core.streamer import FileStreamer
from data_generators.mixing.generator import MixingGenerator


def test_experiment_configs_are_correct(tmp_path):
    file = tmp_path / "file.txt"
    with open("experiment.json", "r") as f:
        conf = json.load(f)
    
    streamer = FileStreamer(str(file))
    mg = MixingGenerator(streamer)

    streams = mg.get_streams(conf["train"], conf["sensor_location"])
    assert streams is None

    