from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todolist.database import get_session
from todolist.models import User
from todolist.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()
database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'olá mundo'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = User(**user.model_dump())
    session.add(db_user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists!!',
        )

    session.refresh(db_user)
    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    session: Session = Depends(get_session),
    limit: int = 10,
    offset: int = 0,
):

    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.get(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def read_user_by_id(user_id: int, session: Session = Depends(get_session)):
    sttm = select(User).where(User.id == user_id)
    user_db: UserPublic = session.scalar(sttm)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found...'
        )

    return user_db


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    sttm = select(User).where(User.id == user_id)
    user_db: UserSchema = session.scalar(sttm)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found...'
        )

    user_db.username = user.username
    user_db.email = user.email
    user_db.password = user.password

    session.add(user_db)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists!!',
        )

    session.refresh(user_db)

    return user_db


@app.delete(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=Message
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    sttm = select(User).where(User.id == user_id)
    user_db = session.scalar(sttm)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found...'
        )

    session.delete(user_db)
    session.commit()

    return {'message': 'User Deleted'}
