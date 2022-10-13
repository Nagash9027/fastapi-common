from fastapi import Depends, APIRouter, status, HTTPException, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth.oauth2 import create_access_token
from database import schemas, models
from database.hash import verify_password
from database.schemas import UserBase, UserDisplay
from database.session import get_db

router = APIRouter(
    prefix='/users',
    tags=['user']
)


@router.post('/', response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return schemas.create_user(db, request)


@router.post('/login')
async def get_token(request: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')

    access_token = create_access_token(data={'sub': user.username})

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_id': user.id,
        'username': user.username
    }
