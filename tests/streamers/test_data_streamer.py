import csv
import io
from core.streamer import FileStreamer


def _write_data_to_file(user_id, columns, data, tmp_path):
    # Create file
    user_id = 1
    _dir = tmp_path / "streamer"
    _dir.mkdir()
    _file = _dir / f"{user_id}.csv"

    out = io.StringIO()
    writer = csv.DictWriter(out, columns)
    writer.writeheader()
    for record in data:
        writer.writerow(record)
    _file.write_text(out.getvalue())

    return _dir, _file


def test_file_streamer(tmp_path):
    user_id = 1
    columns = ["Surface", "Acc_X"]
    data = [
        {"Surface": 1, "Acc_X" :34},
        {"Surface": 1, "Acc_X": 54},
        {"Surface": 2, "Acc_X": 14},
        {"Surface": 2, "Acc_X": 23},
        {"Surface": 3, "Acc_X": 32},
    ]
    _dir, _file = _write_data_to_file(user_id, columns, data, tmp_path)

    surface = 2
    streamer = FileStreamer(str(_dir))
    stream_data = list(streamer.data(user_id, surface))

    with open(_file, "r") as f:
        reader = csv.reader(f)
        for file_record, stream_record in zip(reader, stream_data):
            assert file_record[streamer.SURFACE_COLUMN_IDX] == surface
            assert file_record == stream_record
