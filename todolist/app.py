from http import HTTPStatus

from fastapi import FastAPI

from todolist.routers import auth, users
from todolist.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'olá mundo'}
