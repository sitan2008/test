import datetime
import uuid

from app.database import db
from app.users.models import BaseUser

from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.dialects.postgresql import UUID


class BaseFolder(db.Base):
    __tablename__ = 'folders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    folder_name = Column(String(128), unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime)

    def __init__(self, folder_name, user_id, updated_at=None):
        self.folder_name = folder_name
        self.user_id = user_id
        self.updated_at = updated_at

    def update(self, folder_name: str):
        self.folder_name = folder_name
        self.updated_at = datetime.datetime.utcnow()
