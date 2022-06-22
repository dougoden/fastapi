from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import models, schemas, utils, database, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    query = db.query(models.Users).filter(
        models.Users.email == user_credentials.username)
    result = query.first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication Failed")

    if not utils.verify(user_credentials.password, result.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Authentication Failed")

    access_token = oauth2.create_access_token(data={
        "user_id": result.id
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
