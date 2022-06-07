import datetime
import uuid

from app.database import db
from app.folders.models import BaseFolder

from sqlalchemy import Column, ForeignKey, String, Date, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID


class BaseFile(db.Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = Column(String(128), nullable=False)
    size = Column(Integer, nullable=False)
    type = Column(String(64), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey('folders.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(Date)


    def __init__(self, size, file_name, type, folder_id, updated_at=None):
        self.file_name = file_name
        self.size = size
        self.type = type
        self.folder_id = folder_id
        self.updated_at = updated_at

    def update(self, file_name: str, type: str):
        self.file_name = file_name + '.' + type
        self.updated_at = datetime.datetime.utcnow()

    def move(self, folder_id: UUID):
        self.folder_id = folder_id
