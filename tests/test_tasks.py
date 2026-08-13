from http import HTTPStatus

import pytest

from tests.factories import TaskFactory
from todolist.models import TasksStates
from todolist.schemas import TasksPublic


def test_create_task(client, token):
    response = client.post(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.json() == {
        'id': 1,
        'title': 'Test todo',
        'description': 'Test todo description',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_list_tasks_should_return_5_tasks(session, client, user, token):
    expected_tasks = 5
    tasks = TaskFactory.create_batch(expected_tasks, user_id=user.id)

    session.add_all(tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    expected_json = [
        TasksPublic.model_validate(t, from_attributes=True).model_dump(
            mode='json'
        )
        for t in tasks
    ]

    response = client.get(
        '/tasks/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks
    assert response.json()['tasks'] == expected_json


@pytest.mark.asyncio
async def test_list_tasks_pagination_should_return_2_tasks(
    session, user, client, token
):
    tasks = TaskFactory.create_batch(5, user_id=user.id)
    expected_tasks = 2

    session.add_all(tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    expected_json = [
        TasksPublic.model_validate(t, from_attributes=True).model_dump(
            mode='json'
        )
        for t in tasks[1:3]
    ]

    response = client.get(
        '/tasks/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['tasks']) == expected_tasks
    assert response.json()['tasks'] == expected_json


@pytest.mark.asyncio
async def test_list_tasks_filter_title_should_return_5_tasks(
    session, user, client, token
):
    expected_tasks = 5
    tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, title='Test task 1'
    )
    other_tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, title='Test task 2'
    )

    session.add_all(tasks + other_tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    expected_json = [
        TasksPublic.model_validate(t, from_attributes=True).model_dump(
            mode='json'
        )
        for t in tasks
    ]

    response = client.get(
        '/tasks/?title=Test task 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tasks']) == expected_tasks
    assert response.json()['tasks'] == expected_json


@pytest.mark.asyncio
async def test_list_tasks_filter_description_should_return_5_tasks(
    session, user, client, token
):
    expected_tasks = 5
    tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, description='description'
    )
    other_tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, description='Test task'
    )

    session.add_all(tasks + other_tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    expected_json = [
        TasksPublic.model_validate(t, from_attributes=True).model_dump(
            mode='json'
        )
        for t in tasks
    ]

    response = client.get(
        '/tasks/?description=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tasks']) == expected_tasks
    assert response.json()['tasks'] == expected_json


@pytest.mark.asyncio
async def test_list_tasks_filter_state_should_return_5_tasks(
    session, user, client, token
):
    expected_tasks = 5
    tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, state=TasksStates.draft
    )
    other_tasks = TaskFactory.create_batch(
        expected_tasks, user_id=user.id, state=TasksStates.trash
    )

    session.add_all(tasks + other_tasks)
    await session.commit()

    for task in tasks:
        await session.refresh(task)

    expected_json = [
        TasksPublic.model_validate(t, from_attributes=True).model_dump(
            mode='json'
        )
        for t in tasks
    ]

    response = client.get(
        '/tasks/?state=draft',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['tasks']) == expected_tasks
    assert response.json()['tasks'] == expected_json


def test_delete_task_error(client, token):
    response = client.delete(
        '/tasks/10', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_delete_task(session, client, user, token):
    task = TaskFactory(user_id=user.id)
    session.add(task)
    await session.commit()
    await session.refresh(task)

    response = client.delete(
        f'/tasks/{task.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Task has been deleted successfully.'
    }


@pytest.mark.asyncio
async def test_delete_task_from_other_user(
    session, client, user, other_user, token
):
    task_other_user = TaskFactory(user_id=other_user.id)
    session.add(task_other_user)
    await session.commit()
    await session.refresh(task_other_user)

    response = client.delete(
        f'/tasks/{task_other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


@pytest.mark.asyncio
async def test_patch_task(session, client, user, token):
    task = TaskFactory(user_id=user.id)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    response = client.patch(
        f'/tasks/{task.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


def test_patch_task_error(client, token):
    response = client.patch(
        '/tasks/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
