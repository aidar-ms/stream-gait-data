FROM aidarms/stream-gait:latest

COPY generate_surface_gait_data.py ./generate_surface_gait_data.py

ENV PYTHONPATH ${PYTHONPATH}:.

CMD ["python", "generate_data.py", "-kh", "broker:9092", "-ui", "1,2,3,4,5"]