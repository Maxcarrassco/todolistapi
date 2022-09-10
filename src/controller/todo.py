from fastapi import APIRouter, HTTPException, status, Response, Depends
from src.schema import schemas
from sqlalchemy.orm import Session
from typing import List
from src.model import models
from src.model.db_conn import get_db
from src.auth import auth

router = APIRouter(
    prefix='/api/v1/todos',
    tags=['Todo']
)


@router.get('/', response_model=List[schemas.Todo])
def get_all_todo(db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user), limit: int = 20, skip: int = 0):
    todos = db.query(models.Todos).filter(
        models.Todos.owner_id == user_id).limit(limit).offset(skip).all()
    return todos


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Todo)
def create_post(todo: schemas.CreateTodo, db: Session = Depends(get_db), id: int = Depends(auth.get_active_user)):
    todo = models.Todos(**todo.dict())
    todo.owner_id = id
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get('/{id}/', response_model=schemas.Todo)
def get_todo(id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user)):
    todo = db.query(models.Todos).filter(models.Todos.id == id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if not todo.owner_id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You do not have permission to access this resource")

    return todo


@router.put('/{id}/', response_model=schemas.Todo)
def update_todo(id: int, todo: schemas.CreateTodo, db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user)):
    todo_query = db.query(models.Todos).filter(models.Todos.id == id)
    tododb = todo_query.first()

    if not tododb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if not tododb.owner_id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You do not have permission to modify this resource")

    todo_query.update(todo.dict(), synchronize_session=False)
    db.commit()
    db.refresh(tododb)
    return tododb


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user)):
    todo_query = db.query(models.Todos).filter(models.Todos.id == id)
    tododb = todo_query.first()

    if not tododb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if not tododb.owner_id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You do not have permission to delete this resource")

    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
