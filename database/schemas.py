from datetime import datetime

from fastapi import HTTPException, status, Form
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.hash import get_password_hash
from database.models import Users, Articles, Comments, Channels


# ============================================================================================
class Article(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str
    email: str | None = None
    password: str

    @classmethod
    def as_form(cls,
                username: str = Form(),
                email: str = Form(),
                password: str = Form()):
        return cls(username=username, email=email, password=password)


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str | None = None
    items: list[Article] = []

    class Config:
        orm_mode = True


def create_user(db: Session, request: UserBase):
    exists = db.query(Users).filter(Users.username == request.username).first() is not None
    if exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail='Username already exists')
    new_user = Users(
        username=request.username,
        email=request.email,
        password=get_password_hash(request.password),
        created_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(Users).all()


def get_user(db: Session, id: int):
    user = db.query(Users).get(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user


# ============================================================================================
class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Reply(BaseModel):
    id: int
    created_at: datetime
    content: str
    username: str

    class Config:
        orm_mode = True


class Comment(BaseModel):
    id: int
    created_at: datetime
    content: str
    username: str

    # children: list[Reply] = []

    class Config:
        orm_mode = True


class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: int
    channel_id: int | None = None


class ArticleUpdate(BaseModel):
    title: str
    content: str


class ArticleListDisplay(BaseModel):
    id: int
    title: str
    created_at: datetime
    content: str
    author: User

    class Config:
        orm_mode = True


class ArticleDisplay(BaseModel):
    id: int
    title: str
    created_at: datetime
    content: str
    author: User
    comments: list[Comment]

    class Config:
        orm_mode = True


def create_article(db: Session, request: ArticleBase):
    new_article = Articles(
        title=request.title,
        content=request.content,
        user_id=request.author_id,
        channel_id=request.channel_id,
        created_at=datetime.now()
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def update_article(db: Session, article_id: int, request: ArticleUpdate, user_id: int):
    article = db.query(Articles).get(article_id)

    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Article with id {article_id} not found')
    if article.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only author can update article')

    article.title = request.title
    article.content = request.content
    article.updated_at = datetime.now()

    db.commit()
    db.refresh(article)
    return article


def del_article(db: Session, article_id: int, user_id: int):
    article = db.query(Articles).get(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Article with id {article_id} not found')
    if article.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only author can delete article')
    article.status = 'deleted'
    db.commit()
    return 'ok'


def get_article(db: Session, article_id: int):
    article = db.query(Articles).get(article_id)
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Article with id {article_id} not found')
    return article


def get_all_article(db: Session):
    articles = db.query(Articles).filter(Articles.status == 'active').all()
    if not articles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No article yet')
    return articles


# ============================================================================================
class CommentBase(BaseModel):
    username: str
    content: str
    article_id: int


class ReplyBase(BaseModel):
    username: str
    content: str
    root_id: int


def create_comment(db: Session, request: CommentBase):
    new_comment = Comments(
        content=request.content,
        username=request.username,
        article_id=request.article_id,
        created_at=datetime.now()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def create_reply(db: Session, request: ReplyBase):
    new_reply = Comments(
        content=request.content,
        username=request.username,
        root_id=request.root_id,
        created_at=datetime.now()
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def get_all_comments(db: Session, article_id: int):
    return db.query(Comments).filter(Comments.article_id == article_id).all()


# ============================================================================================
class ChannelBase(BaseModel):
    name: str
    description: str


class ChannelListDisplay(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ChannelDisplay(BaseModel):
    name: str
    description: str

    articles: list[Article]

    class Config:
        orm_mode = True


def create_channel(db: Session, request: ChannelBase):
    new_channel = Channels(
        name=request.name,
        description=request.description,
        created_at=datetime.now()
    )
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    return new_channel


def get_all_channels(db: Session):
    channels = db.query(Channels).filter(Channels.status == 'active').all()
    return channels


def get_articles_in_channel(db: Session, channel_id: int):
    articles = db.query(Articles).filter(Articles.channel_id == channel_id).all()
    return articles
