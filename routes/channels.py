from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import schemas
from database.schemas import ChannelBase, ChannelDisplay, ChannelListDisplay, ArticleDisplay
from database.session import get_db

router = APIRouter(
    prefix='/channel',
    tags=['channel']
)


# create channel
@router.post('/', response_model=ChannelDisplay)
async def create_channel(request: ChannelBase, db: Session = Depends(get_db)):
    return schemas.create_channel(db, request)


# get list
@router.get('/', response_model=list[ChannelListDisplay])
async def get_channels(db: Session = Depends(get_db)):
    return schemas.get_all_channels(db)


# get article list in channel
@router.get('/{channel_id}', response_model=list[ArticleDisplay])
async def get_articles(channel_id: int, db: Session = Depends(get_db)):
    return schemas.get_articles_in_channel(db, channel_id)
