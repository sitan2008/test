from uuid import UUID
from datetime import datetime, date

from pydantic import BaseModel, validator


class FileSchema(BaseModel):
    file_name: str
    size: int
    type: str
    folder_id: UUID


class CreateFile(BaseModel):
    pass


class ReadFile(FileSchema):
    created_at: datetime
    updated_at: date = None

    class Config:
        orm_mode = True


class UpdateFile(BaseModel):
    folder_id: UUID = None
    file_name: str = None


class FileReadAll(BaseModel):
    sort_value: str

    @validator('sort_value')
    def isSortValue(cls, value):
        values = ['file_name', 'size', 'type', 'created_at', 'updated_at']
        if value not in values:
            return None
        return value


class IdFilePath(BaseModel):
    files_id: UUID


class NameFilePatch(BaseModel):
    file_name: str