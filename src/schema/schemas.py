from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str


class CreateUser(UserSchema):
    password: str


class UserResponse(UserSchema):
    #_id: int
    pass


class User(UserSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TodoBase(BaseModel):
    title: str
    description: str


class CreateTodo(TodoBase):
    pass


class Todo(TodoBase):
    pass
