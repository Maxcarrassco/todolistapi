from operator import mod
from typing import List
from fastapi import FastAPI, APIRouter
from src.model import models
from src.model.db_conn import engine
from src.controller import user, todo
from src.auth import auth


app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)
