FROM python:3.9

COPY requirements.txt ./
COPY utils.py ./utils.py

RUN pip install --no-cache-dir -r requirements.txt