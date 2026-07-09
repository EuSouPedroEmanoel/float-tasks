from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    }
