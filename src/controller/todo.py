from fastapi import APIRouter, HTTPException, status, Response, Depends
from src.schema import schemas
from sqlalchemy.orm import Session
from src.model import models
from src.model.db_conn import get_db

router = APIRouter(
    prefix='/api/v1/todos',
    tags=['Todo']
)


@router.get('/')
def get_all_todo(db: Session = Depends(get_db)):
    todos = db.query(models.Todos).all()
    return todos


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_post(todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    todo = models.Todos(**todo.dict())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get('/{id}/')
def get_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todos).filter(models.Todos.id == id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return todo


@router.put('/{id}/')
def update_todo(id: int, todo: schemas.CreateTodo, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todos).filter(models.Todos.id == id)
    tododb = todo_query.first()

    if not tododb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    todo_query.update(todo.dict(), synchronize_session=False)
    db.commit()
    db.refresh(tododb)
    return tododb


@router.delete('/{id}/', status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo_query = db.query(models.Todos).filter(models.Todos.id == id)
    tododb = todo_query.first()

    if not tododb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    todo_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
