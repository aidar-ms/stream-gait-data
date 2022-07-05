
import os

KAFKA_HOST = os.getenv("KAFKA_HOST", "broker:9092")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "stream-gait-data-disser")

