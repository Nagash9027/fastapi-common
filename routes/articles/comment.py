from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from database import schemas
from database.schemas import CommentBase, User, Comment, ReplyBase
from database.session import get_db

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


@router.get('/all/{article_id}', response_model=list[Comment])
async def comments(article_id: int, db: Session = Depends(get_db)):
    return schemas.get_all_comments(db, article_id)


@router.post('')
async def create(request: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return schemas.create_comment(db, request)


@router.post('/r')
async def reply(request: ReplyBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return schemas.create_reply(db, request)
