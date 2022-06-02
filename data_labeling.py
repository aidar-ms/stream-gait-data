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
pattern = re.compile(r"^(\d{1,2})\-000_00B432([\w]{2})\.txt\.csv$")

def label_data(participant_s: int, participant_e: int):
    i = 0

    for n in range(participant_s, participant_e + 1):
        participant_files = list(filter(lambda x: ".txt.csv" in x, os.listdir(f"{data_path}/{n}")))
        print(f"Found {len(participant_files)} files for participant {n}")

        filename = f"labeled_data/{n}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w+") as wf:
            write_doc = csv.writer(wf)
            write_doc.writerow(["Surface", "SensorLocation"] + list(map(str.strip, TrainingSurfaceRecord.column_names)))

            for f_name in participant_files:
                m = pattern.match(f_name)
                surface_code, sensor_location_code = m.group(1), m.group(2)

                with open(f"{data_path}/{n}/{f_name}", "r") as f:
                    doc = csv.reader(f)
                    for row in doc:
                        if len(row) == 0:
                            print("Skipping an empty line")
                            continue
                        elif row[0] == "PacketCounter":
                            print("Skipping a header line")
                            continue

                        write_doc.writerow([TrainingSurfaceRecord.get_surface(surface_code), TrainingSurfaceRecord.get_sensor_location(sensor_location_code)] + list(map(str.strip, row)))
                        i += 1

                        if i % 1000 == 0:
                            print(f"Processed {i} rows for participant {n}")



if __name__ == "__main__":
    ranges = []
    # Split 30 users into 5 buckets
    for j in range(6, 31, 6):
        if j % 6 == 0:
            ranges.append((j-5, j))

    # Label each user bucket data in parallel
    pool = Pool(len(ranges))
    params = [(r[0], r[1]) for r in ranges]
    try:
        pool.starmap(label_data, ((r_s, r_e) for r_s, r_e in ranges))
    except KeyboardInterrupt:
        print("Exiting")
        pool.close()
