from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from todolist.database import get_session
from todolist.models import User
from todolist.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from todolist.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags={'users'})
Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session):

    user_data = user.model_dump()
    user_data['password'] = get_password_hash(user_data['password'])
    db_user = User(**user_data)
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


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(
    current_user: CurrentUser,
    session: Session,
    filter_users: Annotated[FilterPage, Query()],
):

    sttm = select(User).limit(filter_users.limit).offset(filter_users.offset)
    users = session.scalars(sttm)
    return {'users': users}


@router.get('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def read_user_by_id(user_id: int, session: Session):
    sttm = select(User).where(User.id == user_id)
    user_db: UserPublic = session.scalar(sttm)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User Not Found...'
        )

    return user_db


@router.put('/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
):

    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = user.password

    session.add(current_user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists!!',
        )

    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', status_code=HTTPStatus.OK, response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User Deleted'}
