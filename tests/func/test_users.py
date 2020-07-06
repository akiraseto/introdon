import pytest


class TestUser():

    def login(self, client, username, password):
        return client.post('/', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self, client):
        return client.get('/logout', follow_redirects=True)

    def create_user(self, client, username, password):
        return client.post('/user/new', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    init_users = (
        ('2222', '2222'),
        ('Anakin', 'Skywalker'),
        ('LUKE', 'SKYWALKER')
    )

    new_users = (
        ('yoda', 'yoda'),
        ('999999999', '999999999'),
        ('Asajj1', 'Ventress1')
    )

    invalided_users = (
        ('han', 'solo', '4文字以上10文字以内でお願いします'),
        ('DarthTyranus', 'DarthTyranus', '4文字以上10文字以内でお願いします'),
        ('Qui-Gon', 'Jinn', '半角英数のみでお願いします'),
        ('ダースモール', 'ダースモール', '半角英数のみでお願いします')
    )

    task_ids = ['{}-{}'.format(u[0], u[1]) for u in invalided_users]

    def test_admin_login_logout(self, client):
        rv = self.login(client, '1111', '1111')
        assert '管理画面'.encode() in rv.data
        rv = self.logout(client)
        assert 'ログアウトしました'.encode() in rv.data

    @pytest.mark.parametrize(['name', 'pw'], init_users)
    def test_login_logout(self, client, name, pw):
        rv = self.login(client, name, pw)
        assert '参加ゲーム数'.encode() in rv.data
        rv = self.logout(client)
        assert 'ログアウトしました'.encode() in rv.data

    @pytest.mark.parametrize(['name', 'pw'], new_users)
    def test_fail_login(self, client, name, pw):
        rv = self.login(client, name, pw)
        assert '登録が見当たりません'.encode() in rv.data

    @pytest.mark.parametrize(['name', 'pw', 'comment'], invalided_users, ids=task_ids)
    def test_fail_login2(self, client, name, pw, comment):
        rv = self.login(client, name, pw)
        assert comment.encode() in rv.data

    @pytest.mark.parametrize(['name', 'pw'], new_users)
    def test_create_user(self, client, name, pw):
        rv = self.create_user(client, name, pw)
        assert '登録されました!'.encode() in rv.data
        rv = self.logout(client)
        assert 'ログアウトしました'.encode() in rv.data

    @pytest.mark.parametrize(['name', 'pw', 'comment'], invalided_users, ids=task_ids)
    def test_fail_create_user(self, client, name, pw, comment):
        rv = self.create_user(client, name, pw)
        assert comment.encode() in rv.data
