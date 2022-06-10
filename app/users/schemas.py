from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, validator

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserSchema(BaseModel):
    username: str
    password: str


class CreateUser(UserSchema):

    @validator('password')
    def get_password_hash(cls, password):
        return pwd_context.hash(password)


class ReadUser(UserSchema):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class LoginForm(UserSchema):
    pass
