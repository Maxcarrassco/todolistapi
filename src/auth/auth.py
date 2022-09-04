from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from src.model.db_conn import get_db
from src.model import models
from src.schema import schemas
from src.utils.hashed import verify_pwd
from src.auth.oauth2 import create_token, get_active_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/api/v1/auth',
    tags=['Authentication']
)


@router.post('/', response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = db.query(models.User).filter(
        models.User.username == user.username).first()

    if not user_db:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Wrong password or username")
    if not verify_pwd(user.password, user_db.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Wrong password or username")
    access_token = create_token({"user_id": user_db.id})
    token = schemas.TokenCreate(access_token, "Bearer")
    return token


@router.get('/me', response_model=schemas.User)
def get_current_user(user_id: int = Depends(get_active_user), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user credential",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user
