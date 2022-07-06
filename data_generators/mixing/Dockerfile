FROM aidarms/stream-gait:latest

COPY generator.py ./generator.py
COPY run.py ./run.py

ENV PYTHONPATH ${PYTHONPATH}:.

CMD ["python", "run.py", "-st", "s3", "-sn", "stream-gait-data-disser", "-dt", "file", "-dn", "generated_data.txt"]