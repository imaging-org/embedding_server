from minio import Minio
from utils.config import MinioConfig

from io import BytesIO
from PIL import Image


class MinioService:
    def __init__(self):
        self._client = Minio(
            "localhost:9000",
            access_key=MinioConfig.ACCESS_KEY,
            secret_key=MinioConfig.SECRET_KEY,
            secure=False
        )

    def get_file(self, object_key):
        print(f"Getting file from Minio : {object_key}")

        data = BytesIO()

        response = self._client.get_object(
            MinioConfig.BUCKET_NAME,
            object_key
        )
        data.write(response.data)
        data.seek(0)

        image = Image.open(data)

        response.close()
        response.release_conn()

        return image

