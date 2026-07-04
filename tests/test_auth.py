from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_raise_login_for_acess_token_not_found_user(client):
    response = client.post(
        '/auth/token',
        data={
            'username': 'test',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_raise_login_for_acess_token_incorrect_password(client, user):
    response = client.post(
        '/auth/token',
        data={
            'username': f'{user.username}',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
