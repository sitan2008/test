from uuid import UUID

from pydantic import BaseModel


class File(BaseModel):
    file_name: str
    size: int
    type: str
    folder_id: UUID