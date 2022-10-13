from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from fractions import Fraction

from database import models, schemas
from database.schemas import UserDisplay
from database.session import engine, get_db
from routes import channels
from routes.users import user
from routes.articles import article, comment

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user.router)
app.include_router(article.router)
app.include_router(comment.router)
app.include_router(channels.router)


@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.get('/{user_id}', response_model=UserDisplay)
async def get(user_id: int, db: Session = Depends(get_db)):
    return schemas.get_user(db, user_id)


origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

models.Base.metadata.create_all(engine)
