from http import HTTPStatus

from todolist.schemas import UserPublic


def test_root_deve_retornar_ola_mundo(client):

    response = client.get('/')
    assert response.json() == {'message': 'olá mundo'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@exemple.com',
            'password': 'S3cr3t!123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@exemple.com',
    }


def test_create_user_integraty(client):
    client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'fausto@exemple.lol',
            'password': 'secret',
        },
    )

    actual_update = client.post(
        '/users/',
        json={
            'username': 'fausto',
            'email': 'bob@exemple.lol',
            'password': 'newsecret',
        },
    )

    assert actual_update.status_code == HTTPStatus.CONFLICT
    assert actual_update.json() == {
        'detail': 'Username or Email already exists!!'
    }


def test_read_users_blank(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_fill(client, user):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id(client, user):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Teste',
        'email': 'test@test.com',
        'id': 1,
    }


def test_raise_read_user_by_id(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found...'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Pedro',
            'email': 'pedro@email.ai',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Pedro',
        'email': 'pedro@email.ai',
        'id': 1,
    }


def test_update_integrity_error(client, user):
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@exemple.lol',
            'password': 'secret',
        },
    )

    actual_update = client.put(
        f'/users/{user.id}',
        json={
            'username': 'fausto',
            'email': 'bob@exemple.lol',
            'password': 'newsecret',
        },
    )

    assert actual_update.status_code == HTTPStatus.CONFLICT
    assert actual_update.json() == {
        'detail': 'Username or Email already exists!!'
    }


def test_delete_user(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_raise_update_user(client):
    response = client.put(
        '/users/2',
        json={
            'username': 'Pedro',
            'email': 'blablabla@email.com',
            'password': 'senha',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_raise_delete_user(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
