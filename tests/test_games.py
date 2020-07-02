import os

import pytest

import introdon
from introdon.scripts.db import InitDB


# todo:pytest-flask
# todo:pytest-coverage
# todo:pytest-codestyle


@pytest.fixture
def client():
    # 環境変数がTESTでないなら、エラー起こして止める
    if os.environ['ENV'] != 'TEST':
        raise

    # form.validate_on_submit()解除に必要
    introdon.app.config['WTF_CSRF_ENABLED'] = False
    introdon.app.config['DEBUG'] = True
    introdon.app.config['TESTING'] = True

    # 全部消す
    introdon.db.drop_all()
    InitDB().run()

    for line in open('tests/sql/introdon_users.sql'):
        introdon.db.session.execute(line)

    for line in open('tests/sql/introdon_songs.sql'):
        introdon.db.session.execute(line)

    for line in open('tests/sql/introdon_games.sql'):
        introdon.db.session.execute(line)

    for line in open('tests/sql/introdon_logs.sql'):
        introdon.db.session.execute(line)

    with introdon.app.test_client() as client:
        with introdon.app.app_context():
            yield client

    introdon.db.session.close()


def login(client, username, password):
    return client.post('/', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def create_user(client, username, password):
    return client.post('/user/new', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_admin_login_logout(client):
    rv = login(client, '1111', '1111')
    assert '管理画面'.encode() in rv.data

    rv = logout(client)
    assert 'ログアウトしました'.encode() in rv.data


def test_login(client):
    rv = login(client, '2222', '2222')
    assert '参加ゲーム数'.encode() in rv.data


def test_create_user(client):
    rv = create_user(client, 'hansolo', 'leiaorgana')
    assert '登録されました!'.encode() in rv.data
