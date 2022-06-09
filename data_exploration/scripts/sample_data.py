"""
Script that does the following:
- labels each data row with surface type and sensor location
- gathers data for each participant in a single CSV file

Currently, there are no plans to use this script in the Kafka pipeline. It simply makes it easier to use data in offline analysis with Jupyter notebook
"""

import os, re, csv
from records.surface import TrainingSurfaceRecord
from multiprocessing import Pool

data_path = "input_data_SD"
pattern = re.compile(r"^(\d{1,2})\-000_00B4328B\.txt\.csv$")

def label_data(participant_s: int, participant_e: int):
    filename = f"sampled_data/data.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w+") as wf:
        write_doc = csv.writer(wf)
        write_doc.writerow(["UserId"] + list(map(str.strip, TrainingSurfaceRecord.column_names)))

        for n in range(participant_s, participant_e + 1):
            participant_files = list(filter(lambda x: ".txt.csv" in x, os.listdir(f"{data_path}/{n}")))
            print(f"Found {len(participant_files)} files for participant {n}")

            for file_name in participant_files:
                i = 0
                m = pattern.match(file_name)
                if m is None:
                    continue

                surface_code, sensor_location_code = m.group(1), "8B"
                with open(f"{data_path}/{n}/{file_name}", "r") as f:
                    doc = csv.reader(f)
                    for row in doc:
                        if len(row) == 0 or row[0] == "PacketCounter":
                            continue

                        if i >= 1000:
                            print(f"Processed {i} rows for participant {n}, surface {surface_code} and sensor {sensor_location_code}. Stopping now...")
                            break

                        write_doc.writerow(
                            [
                                n,
                                TrainingSurfaceRecord.get_surface(surface_code),
                                TrainingSurfaceRecord.get_sensor_location(sensor_location_code)
                            ] + list(map(str.strip, row))
                        )

                        i += 1


if __name__ == "__main__":
    ranges = []
    label_data(1, 30)