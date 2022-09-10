from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str


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
    id: int
    iscompleted: bool
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenCreate:
    def __init__(self, access_token: str, token_type: str) -> None:
        self.access_token = access_token
        self.token_type = token_type
