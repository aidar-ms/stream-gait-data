import io
import json

import pytest

from kafka import KafkaConsumer

from core.emitter import Emitter
from core.receiver import Receiver


def test_receiver_init_file(tmp_path):
    # Create dir
    file_dir = tmp_path / "receiver_data"
    file_dir.mkdir()
    # Create file
    file_name = "file.json"
    file = file_dir / file_name
    data = [{"a": 12, "b" :34}, {"a": 23, "b": 54}]

    file.write_text("\n".join(map(json.dumps, data)))

    r = Receiver("file", str(file))
    assert isinstance(r.handle, io.IOBase)

    # Check the contents
    for streamed, original in zip(r.stream, data):
        assert streamed == original

    r.close()


@pytest.mark.timeout(5)
def test_receiver_kafka():
    topic_name = "kafka-topic"
    r = Receiver("kafka", topic_name)
    assert isinstance(r.handle, KafkaConsumer)
    r.close()


def test_emitter_file(tmp_path):
    # Create dir
    file_dir = tmp_path / "emitter_data"
    file_dir.mkdir()

    # Generate mock data
    file_name = "emitted_data.txt"
    data = [{"a": 12, "b" :34}, {"a": 23, "b": 54}, {"a": 53, "b": 104}]

    # Send data via Emitter
    _file = file_dir / file_name
    e = Emitter(Emitter.DEST_FILE, str(_file))
    for record in data:
        e.send(record)

    assert _file.is_file()

    e.close()
