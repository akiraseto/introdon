import pytest

from introdon.models.games import Game
from introdon.models.logs import Log
from introdon.models.songs import Song


# 全網羅は無理! funcテストていない箇所で、かつ重要そうな箇所のみ

# circleCI用にmockを使ったunitテストを準備する
# テストmarkして、circleCIではそれだけをテスト
# circleCIでは、unitテストかつ、mockのみ(最終的に自動CDする為)


class TestUnits():

    @pytest.mark.parametrize('game_id, expected', [
        pytest.param(4, [2, 1], id='multi_user'),
        pytest.param(1, [1], id='one_user')
    ])
    def test_fetch_users_id(self, client, game_id, expected):
        game_instance = Game.query.filter(Game.id == game_id).first()
        result = Game.fetch_users_id(game_instance)

        assert expected == result

    def test_calc_score(self, client):
        game_id = 5
        users_id_list = [2, 1]
        expected = [(1, 240), (2, 230)]

        result = Log.calc_score(game_id, users_id_list)
        assert expected == result

    @pytest.mark.use_mock
    def test_add_song(self, mocker):
        # ダミーのレスポンス作成
        responseMock = mocker.Mock()
        responseMock.status_code = 404
        # requests.getの戻り値をpatch
        mock_res = mocker.patch('requests.get')
        mock_res.return_value = responseMock

        term = 'Shmi'
        attribute = ' Skywalker'
        limit = 9
        validate, status_code = Song.add_song(term, attribute, limit)

        assert validate == False
        assert status_code == 404
