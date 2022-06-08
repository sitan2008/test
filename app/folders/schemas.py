from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class FolderSchema(BaseModel):
    folder_name: str


class CreateFolder(FolderSchema):
    user_id: UUID


class ReadFolder(CreateFolder):
    id: UUID
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True


class UpdateFolder(FolderSchema):
    pass


class IdFolderPath(BaseModel):
    folder_id: UUID


class NameFolderPatch(BaseModel):
    folder_name: str
