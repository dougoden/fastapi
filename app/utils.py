from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password_plaintext, password_hashed):
    return pwd_context.verify(password_plaintext, password_hashed)
