from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    password: str


class CreateUser(UserSchema):
    pass


class ReadUser(UserSchema):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class LoginForm(BaseModel):
    login: str
    password: str