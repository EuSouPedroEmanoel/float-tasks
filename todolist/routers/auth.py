from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from todolist.database import get_session
from todolist.models import User
from todolist.schemas import Token
from todolist.security import create_access_token, verify_password

router = APIRouter(prefix='/auth', tags={'auth'})

Session = Annotated[Session, Depends(get_session)]
OAuthForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuthForm, session: Session):
    sttm = select(User).where(User.username == form_data.username)
    user = session.scalar(sttm)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Username or Password is wrong',
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Username or Password is wrong',
        )

    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'Bearer'}
