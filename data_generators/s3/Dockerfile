FROM aidarms/stream-gait:latest

COPY generate_data.py ./generate_data.py

ENV PYTHONPATH ${PYTHONPATH}:.

CMD ["python", "generate_data.py", "-kh", "broker:9092", "-ui", "1,2,3,4,5"]