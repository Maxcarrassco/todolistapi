from typing import List
from fastapi import APIRouter, HTTPException, status, Response, Depends
from src.schema import schemas
from sqlalchemy.orm import Session
from src.model import models
from src.model.db_conn import get_db
from src.utils.hashed import hashed_pwd
from src.auth import auth


router = APIRouter(
    prefix="/api/v1/users",
    tags=["User"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    user.password = hashed_pwd(user.password)
    usr = models.User(**user.dict())
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db), _: int = Depends(auth.get_active_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    return user


@router.put('/{id}')
def update_user(id: int, usr: schemas.CreateUser, db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if not user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You do not have permission to modify this resource")

    user_query.update(usr.dict(), synchronize_session=False)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(auth.get_active_user)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    if not user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="You do not have permission to delete this resource")

    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
