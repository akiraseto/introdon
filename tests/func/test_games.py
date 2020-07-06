import pytest


class TestGame():

    @pytest.fixture()
    def login_1111(self, client):
        return client.post('/', data=dict(
            username=1111,
            password=1111
        ), follow_redirects=True)

    start_params = (
        ('', '', '1900', '2100'),  # 未指定
        ('Perfume', '', '1900', '2100'),  # 既存曲
        ('エアロスミス', '', '1900', '2100'),  # 未登録曲
        ('', 'J-Pop', '1900', '2100'),  # 既存ジャンル
        ('', 'クラシック', '1900', '2100'),  # 未登録ジャンル
        ('', '', '2000', '2010'),  # 年代しぼり
    )

    # ひとりで遊ぶ
    @pytest.mark.parametrize(['artist', 'genre', 'release_from', 'release_end'], start_params)
    def test_start_game_alone(self, client, artist, genre, release_from, release_end):
        rv = client.post('/game/setting', data=dict(
            artist=artist,
            genre=genre,
            release_from=release_from,
            release_end=release_end,
        ), follow_redirects=True)

        assert '問 /10'.encode() in rv.data

    # みんなであそぶ:未指定
    @pytest.mark.usefixtures('login_1111')
    def test_start_game_multi(self, client):
        with client.session_transaction() as sess:
            sess['creatable'] = True

        rv = client.post('/game/start_multi', data=dict(
            artist='',
            genre='',
            release_from='1900',
            release_end='2100',
        ), follow_redirects=True)

        assert 'メンバー受付中・・'.encode() in rv.data

    @pytest.mark.usefixtures('login_1111')
    def test_failure_multi(self, client):
        rv = client.get('/game/failure_multi', follow_redirects=True)
        assert 'ゲーム不成立..'.encode() in rv.data

    @pytest.mark.parametrize('game_id, expected', [
        pytest.param(1, [['1111', 530, 0.35]]),
        pytest.param(5, [['1111', 530, 0.35], ['2222', 310, 0.37]])
    ])
    def test_participating_members(self, client, game_id, expected):
        game_id = game_id

        rv = client.get('/game/participating_members?game_id=' + str(game_id))
        assert rv.json == expected
