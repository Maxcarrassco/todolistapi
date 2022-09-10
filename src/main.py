from operator import mod
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller import user, todo
from src.auth import auth


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(todo.router)
app.include_router(auth.router)


app.get('/')


def home():
    return {"deployed": True}
