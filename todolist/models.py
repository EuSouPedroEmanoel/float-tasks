from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from sqlalchemy.orm import validates

table_registry = registry()


class TasksStates(str, Enum):
    draft = 'draft'
    task = 'task'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass()
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    tasks: Mapped[list[Task]] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )


@table_registry.mapped_as_dataclass()
class Task:
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TasksStates]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    @validates('state')
    def validate_state(self, key, value):
        if isinstance(value, str) and not isinstance(value, TasksStates):
            return TasksStates(value)
        return value
