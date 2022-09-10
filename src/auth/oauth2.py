from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from src.env import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth')
SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_token(credential_exception, token: str) -> int:
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,
                             algorithms=[ALGORITHM])
        # if not payload:
        #raise credential_exception
        user_id: int = payload.get('user_id')
        if not user_id:
            raise credential_exception
    except JWTError:
        raise credential_exception
    return user_id


def get_active_user(token: str = Depends(oauth2_scheme)) -> int:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate user credential",
        headers={"WWW-Authenticate": "Bearer"}
    )

    return verify_token(credential_exception=credential_exception, token=token)
