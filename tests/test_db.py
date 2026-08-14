from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from tests.factories import TaskFactory
from todolist.models import User


@pytest.mark.asyncio
async def test_create_user(session: AsyncSession, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='test', email='test@test', password='secret')

        session.add(new_user)
        await session.commit()

        sttm = select(User).where(User.username == 'test')

        user = await session.scalar(sttm)

    assert asdict(user) == {
        'id': 1,
        'username': 'test',
        'email': 'test@test',
        'password': 'secret',
        'created_at': time,
        'updated_at': time,
        'tasks': [],
    }


@pytest.mark.asyncio
async def test_wrong_enum_in_create_task(user, session):
    with pytest.raises(ValueError, match='is not a valid TasksStates'):
        TaskFactory.build(user_id=user.id, state='invalid')
