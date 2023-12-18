from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from auth.oauth2 import get_current_user
from database import schemas
from database.schemas import ArticleBase, ArticleDisplay, User, ArticleUpdate, ArticleListDisplay
from database.session import get_db

router = APIRouter(
    prefix='/article',
    tags=['article']
)


@router.post('/', response_model=ArticleDisplay)
async def create_article(request: ArticleBase, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    return schemas.create_article(db, request)


@router.post('/u/{article_id}', response_model=ArticleDisplay)
async def up_article(article_id: int, request: ArticleUpdate, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return schemas.update_article(db, article_id, request, current_user.id)


@router.get('/a/{article_id}', response_model=ArticleDisplay)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    return schemas.get_article(db, article_id)


@router.get('/all', response_model=list[ArticleListDisplay])
async def get_all_articles(db: Session = Depends(get_db)):
    return schemas.get_all_article(db)


@router.delete('/{article_id}')
async def del_article(article_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    return schemas.del_article(db, article_id, current_user.id)
