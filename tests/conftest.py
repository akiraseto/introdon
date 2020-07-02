import os

import pytest

import introdon
from introdon.scripts.db import InitDB


# todo:pytest-flask
# todo:pytest-coverage
# todo:pytest-codestyle


@pytest.fixture(scope='session')
def client():
    # 環境変数がTESTでないなら、エラー起こして止める
    if os.environ['ENV'] != 'TEST':
        raise

    # form.validate_on_submit()解除に必要
    introdon.app.config['WTF_CSRF_ENABLED'] = False
    introdon.app.config['TESTING'] = True

    # データ全消去
    introdon.db.drop_all()
    # Tableの初期化
    InitDB().run()

    # テストDATAのインサート
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
