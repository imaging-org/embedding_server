from dataclasses import dataclass
from os import getenv


@dataclass
class MinioConfig:
    ACCESS_KEY = getenv("ACCESS_KEY", "qLU7Yb5jfyXmHQhUyRb5")
    SECRET_KEY = getenv("SECRET_KEY", "FEAVIoGFuY179WzrGkYhj9swt3IMjCqb8cwFP5db")
    BUCKET_NAME = getenv("BUCKET_NAME", "test-bucket")
