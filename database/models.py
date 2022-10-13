from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship, validates

from database.session import Base


class BaseMixin:
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum('active', 'deleted', 'blocked'), default='active')
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Users(Base, BaseMixin):
    __tablename__ = 'users'
    username = Column(String, unique=True, index=True)
    email = Column(String)
    password = Column(String)

    items = relationship('Articles', back_populates='author')

    # 게시글 스크랩 기능 추가
    # 리스트 즐겨찾기?


# class UsersA(Base, BaseMixin):
#     __tablename__ = 'users_a'
#     username = Column(String, uniques=True, index=True)
#     email = Column(String)
#     password = Column(String)


class Articles(Base, BaseMixin):
    __tablename__ = 'articles'
    title = Column(String)
    content = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('Users', back_populates='items',
                          uselist=False)

    comments = relationship('Comments', back_populates='article')

    # 관계 >> 리스트
    channel_id = Column(Integer, ForeignKey('channels.id'))
    channel = relationship('Channels', back_populates='articles',
                           uselist=False)
    # 설정 여부


class Channels(Base, BaseMixin):
    __tablename__ = 'channels'
    name = Column(String)
    description = Column(String)

    # members = relationship('', back_populates='') >> 우선은 공용 채널 >> 카테고리 형식 => 차후 멤버 단위 설정
    articles = relationship('Articles', back_populates='channel')


class Comments(Base, BaseMixin):
    __tablename__ = 'comments'
    content = Column(String)
    username = Column(String)

    article_id = Column(Integer, ForeignKey('articles.id'), index=True)
    article = relationship('Articles',
                           back_populates='comments',
                           uselist=False)

    root_id = Column(Integer, ForeignKey('comments.id'))
    root = relationship('Comments',
                        back_populates='children',
                        remote_side='Comments.id',
                        primaryjoin='Comments.id==Comments.root_id',
                        uselist=False)

    children = relationship('Comments',
                            back_populates='root',)

    # 대댓글 기능을 위한 reply 관련 요소 -> 자기 자신을 부모 혹은 자식으로 둘 수 있게


"""
1. 리스트와 연결을 통해 권한을 제공: Member, ChannelRights
    a. Members (members) >> 멤버, <> 채널, < 채널 권한
    b. ChannelRights (channel_rights) >> 권한, > 채널, > 멤버 / 채널 생성시 >>> 기본:생성자, 관리자, 일반 3테이블 생성
        : 채널 삭제, 채널 편집, 게시글 삭제, 게시글 설정, 권한 관리, 유저 차단
"""
