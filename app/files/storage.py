from minio import Minio

from app import config

cfg = config.MinioConfig()


class MINIO:
    def __init__(self):
        self.bucket = Minio(
            endpoint=cfg.MINIO_URL,
            secret_key=cfg.SECRET_KEY,
            access_key=cfg.ACCESS_KEY,
            secure=False)
        self.bucket_name = cfg.BUCKET_NAME

    def init_bucket(self):
        found = self.bucket.bucket_exists(self.bucket_name)
        if not found:
            self.bucket.make_bucket(self.bucket_name)

    def load_file(self, file_name: str, file, size: int):
        self.bucket.put_object(self.bucket_name, file_name, file, size)

    def share_file_link(self, file_name: str):
        link = self.bucket.presigned_get_object(self.bucket_name, file_name)
        return link

    def download_file(self, file_name: str):
        file = self.bucket.get_object(self.bucket_name, file_name)
        return file

    def update_file(self, new_name: str, file_name: str, size: int, type: str):
        file = self.download_file(file_name)
        name = new_name + '.' + type
        self.load_file(name, file, size)
        self.delete_file(file_name)

    def delete_file(self, file_name: str):
        self.bucket.remove_object(self.bucket_name, file_name)
