from pydantic import BaseModel, ConfigDict, EmailStr, Field

from todolist.models import TasksStates


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
# region - Token
class Token(BaseModel):
    token_type: str
    access_token: str


# endregion
# region - Filters
class FilterPage(BaseModel):
    limit: int = Field(ge=1, default=10)
    offset: int = Field(ge=0, default=0)


class FilterTask(FilterPage):
    title: str | None = Field(None, min_length=3)
    description: str | None = None
    state: TasksStates | None = None


# endregion
# region - Tasks
class TasksSchema(BaseModel):
    title: str
    description: str
    state: TasksStates = Field(default=TasksStates.task)


class TasksPublic(TasksSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TaskList(BaseModel):
    tasks: list[TasksPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TasksStates | None = None


# endregion
