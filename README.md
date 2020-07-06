# introdon
イントロドン:曲当てクイズ

Flask
nginx
gunicorn
(vue.js)

MySQL

# itunes api
https://itunes.apple.com/search

sqlalcemmyが必要とする
conda install pymysql

# docker-compose up 後に containerにattachする
docker exec -it ID_OR_NAME bash

# Listenしているポートを確認する
sudo lsof -i -P | grep "LISTEN"

# MACのapache2を停める
sudo apachectl stop

# UnitTest
CircleCI,ローカルで直にテストする場合
(Dockerを利用しない場合)
OSの環境変数をセットする必要がある

export FLASK_ENV=TEST && pytest -m 'use_mock'
