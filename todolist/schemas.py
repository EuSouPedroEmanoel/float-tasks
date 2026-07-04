from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


# region - User
class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    username: str
    email: EmailStr
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


# endregion


class Token(BaseModel):
    token_type: str
    access_token: str


class FilterPage(BaseModel):
    limit: int = Field(ge=1, default=10)
    offset: int = Field(ge=0, default=0)
