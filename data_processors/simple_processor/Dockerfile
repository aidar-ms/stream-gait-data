FROM aidarms/stream-gait:latest

COPY processor.py ./processor.py
COPY run.py ./run.py

ENV PYTHONPATH ${PYTHONPATH}:.

CMD ["python", "run.py"]