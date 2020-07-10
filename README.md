# 『クイズ・イントロドン!!』
曲当てクイズアプリ  

公開ページ:  
http://introdon.akinko.work/


## ゲーム内容
- 曲のイントロが流れるので4択の中から曲名を当てるゲーム
- 全部で10問出題
- できるだけ多くの正解を目指そう!


### 進め方
- アカウント登録する
    - ログイン後に、プレイモード:「ひとりで遊ぶ」,「みんなで遊ぶ」を選んでプレイ
- アカウント登録しない
    - 「簡易版で遊ぶ」を選んでプレイ


### プレイモード

- ひとりモード
    - 時間制限なしでじっくりと解答
    - アカウント作成しなくても簡易版からゲームできる
        - 但し、解答数や正解率など成績は残らない。
    
- みんなでモード
    - 最大5人参加の早押しクイズ
    - 正解順に得点が分配され10問答えた後に合計得点でランキングされる
    - 不正解はもちろん0point、なるべく早く答えつつも正解を目指そう
    - アカウント作成しないと参加できない。


### ゲームのポイント

- ユーザー登録するorしない?
    - 登録することで解答数やゲーム参加回数、正解率が記録される
    - 「みんなでモード」は登録しないとプレイできない
    - 「簡易版で遊ぶ」からひとりモードをプレイできるが、成績は記録できない。

- 出題内容:「問題を作ろう」
    - 何も入力せずにスタート
        - DBに溜まった曲からランダムに出題される
    - 出題を絞る:アーティスト、ジャンルを入力、年代を選択
        - 絞られた内容で問題を作成し出題される。
        - 曲がDBに無い、足りない場合は、apiを通じて曲を取得しDBに登録し出題する。  
        **みんなが検索すればするほど登録曲が増えていきバリエーションが豊富になります**

- ゲーム環境: PCブラウザ、スマートフォン
    - スマホ版は、各社のブラウザ規約により、楽曲の自動再生が禁止・不可です
        - 出題毎に、「音楽を再生♪」をタップしてください。
        - 正直、「みんなで遊ぶ」モードはPC版の方が有利になります。
    - PC版は楽曲は自動で再生されます。


---
# Develop内容

## ゲームの初期設定


### 1.ファイル修正
以下のファイルに任意の値を追加して、リネームしてください  
```sh
mv db/envfile.sample db/envfile
```


### 2.docker-compose
docker、及びdocker-composeが必要となります。環境に事前にインストールしてください。  
ルートディレクトリで以下を実行
```sh
docker-compose up -d
```

flask container build中にWarningが出ますが問題ありません。  
Pipenvでインストールしているのですが、Python仮想環境が見つからないため出るWarningです。
`--system`オプションでpython仮想環境は使わずにDocker環境に直接インストールしています。


### 3.アプリアップ
localhost(127.0.0.1)でアプリが立ち上がります。

失敗する場合は、PORT番号がぶつかっている可能性があります。  
このアプリは、PORT:**80**を使用しています。
空いているportを調べて、以下の箇所を任意の番号に変更します。

```yaml
#docker-compose.yml

services:
  nginx:
    build: nginx
    container_name: nginx
    ports:
      - "80:80"
       # ↑左のホスト側の80を任意の番号に変更
```
 
Listenしているポートを確認する
```
sudo lsof -i -P | grep "LISTEN"
```
  
または、事前に80番使っているアプリを停止する。  
MACのapache2を停める
```
sudo apachectl stop
```


### 4.DBを初期化
まだプレイできません。DBを初期化する必要があります。
flask containerからDBの全Table作成の初期化を実行します。

以下の、`ID_OR_NAME`の箇所に`flask`を入力してcontainerにattachします。
```
docker exec -it ID_OR_NAME bash
```

flask container内のコンテンツルートディレクトリで以下を実行
```
python manage.py init_db
```

これで、DBが初期化されて、ゲームをプレイできるようになります。


## 管理画面に関して
管理画面でできること。

- DBデータの閲覧
- 楽曲の手動追加
- admin権限の付与

admin権限のあるユーザーのみ、管理画面ボタンが表示されて入ることが出来ます。  
`アプリヘッダー > 管理画面 (ログアウトの左)`

最初のadmin権限ユーザーはセキュリティ上、DBの直接操作からのみ作れるようにしました。


### 1.DB containerにattach、
```
docker exec -it mariadb bash
```


### 2.DBにログインして、user tableで権限付与したいユーザーのadmin columnを1に変更。
```
#ユーザー パスワードを入力してDBにログイン
mysql -uXXXXXXXX -pXXXXXXX

#使用DBを選択
USE introdon;

#admin columnを0から1に変更
UPDATE users SET admin = 1 WHERE  username = 'XXXXX';
```

これで、該当ユーザーはadmin権限を持ち、管理画面に入ることが出来ます。

2人目以降は、
`管理画面 > User > editボタン > admin チェックボタン`から管理者を増やすことが出来ます。


---
# 技術メモ

## 環境変数 PROD DEV TEST
以下の環境変数の変更で3種のモードが実行される  
`docker-compose > flask > FLASK_ENV`

- PROD  
    - プロダクションモード。いわゆる本番用
    - Flask:Debug=False, GunicornでWSGIしてNginxでレンダーされる
- DEV  
    - Developモード。つまり開発モード
    - Flask:Debug=True, WSGI使わずNginxでレンダーされる
    - アプリ描画にはdebug toolbarが表示され、関係する変数が確認できる
- TEST  
    - テストモード
    - flask containerを通して、function,unitテストを自動で実行する
    - 上記2つと異なり、テスト用のDB containerを使用する。
    - テストDB containerは、データは永続化せず、実行ごとに初期化される


## データ永続化 (volume)
PROD,DEVモードは、docker_dataディレクトリが自動で生成されデータが永続化される。  
DBデータ、各ログデータの2種が以下の構成でローカルに保存される。

```
docker_data/
├── log
│   ├── flask
│   │   ├── gunicorn_access.log
│   │   └── gunicorn_error.log
│   ├── mysql
│   │   └── mysql.log
│   └── nginx
│       ├── access.log
│       └── error.log
└── mysql

```


## フロントエンド
Jinja2とVue.jsの組み合わせで作成  

Vue.jsは単一ファイルコンポーネントを使わず、CDNにてtemplateのhtmlに実装。  
CDNはProductionモードにしているが、`introdon/templates/layout.html`から、devモードのCDNに変更可能。


## CircleCI
unitテストのみ実行可

以下の箇所を補足説明
```yaml
# .circleci/config.yml
  - run:
      name: run tests
      command: |
        export FLASK_ENV=TEST
        export MYSQL_USER=dummy
        export MYSQL_PASSWORD=dummy
```
circleCIの実行環境に環境変数を追加

- export FLASK_ENV=TEST  
    docker-compose.ymlではPRODにしているため、テスト実行用に変更
- export MYSQL_USER=dummy
- export MYSQL_PASSWORD=dummy  
    unitテストはmock使用でDB不使用のため適当な環境変数を入れている

メモ:
CircleCIのmachineによるdocker-compose展開でfuncテストも検討したが、
push時にテストを走らせるためFLASK_ENV=TEST,CircleCI後にPRODに変更と煩わしいため不採用とした。
また、CircleCIの無料枠だとdocker buildのcacheが効かないため毎回のテスト時間も多く、加えてmachineが有料になる可能性もあるようでその点も考慮し今回はお見送り。


## pytestのローカルテスト

### Dockerで一括テスト
以下の環境変数をPRODからTESTに変更  
`docker-compose > flask > FLASK_ENV: TEST`

`docker-compose up`でfuncテスト、unitテストが走りcoverageが吐き出される。

テストエラーが多い場合は、DBが準備ができていない可能性が高い。
DB container立ち上がり後に、再度flask container を立ち上げてテストする。


### UnitTestのみテスト(Dockerを利用しない)
OSの環境変数をセットする必要があるため、以下を実行
```
export FLASK_ENV=TEST && pytest -m 'use_mock'
```


## そもそも楽曲はどこから入手か?
itunes api  
https://itunes.apple.com/search
