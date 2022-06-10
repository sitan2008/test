import datetime
import uuid

from passlib.context import CryptContext

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from app.database import db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseUser(db.Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def verify_password(plain_password, hashed_password) -> str:
        return pwd_context.verify(plain_password, hashed_password)


