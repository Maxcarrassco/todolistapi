import pwd
from passlib.context import CryptContext

pwd_context = CryptContext(schemes='bcrypt')


def hashed_pwd(password: str) -> str:
    return pwd_context.hash(password)


def verify_pwd(user_pass: str, hashed_pass: str) -> bool:
    return pwd_context.verify(user_pass, hashed_pass)
