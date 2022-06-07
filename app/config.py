import os

from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:

    def __init__(self):
        self.host = os.environ.get("DB_HOST", "5432")
        self.port = os.environ["DB_PORT"]
        self.name = os.environ["DB_NAME"]
        self.user = os.environ["DB_USER"]
        self.password = os.environ["DB_PASSWORD"]
        self.engine = "postgresql+psycopg2://"

    def get_db_url(self) -> str:
        return self.engine + self.user + ":" + self.password + "@" + self.host + ":" + self.port + "/" + self.name


class MinioConfig:

    def __init__(self):
        self.ACCESS_KEY = os.environ['ACCESS_KEY']
        self.SECRET_KEY = os.environ['SECRET_KEY']
        self.MINIO_URL = os.environ['MINIO_URL']
        self.BUCKET_NAME = os.environ['BUCKET_NAME']