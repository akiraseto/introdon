import random

from flask import redirect, url_for, render_template, flash, session

from introdon import app, db
from introdon.models.games import Game
from introdon.models.songs import Song, SongSchema

MAX_QUESTION = 10
MAX_SELECT = 4


@app.route('/')
# @login_required
def setting_game():
    # todo:ここに曲の絞り込みを書く

    return render_template('games/index.html')


@app.route('/games/start', methods=['POST'])
# @login_required
def start_game():
    # gameをgenerateしてDBに保存する
    # songDBのレコード数をカウント
    songs_count = Song.query.count()

    # 登録曲が少なすぎる場合は「曲が少なくて作れません」
    if songs_count < MAX_QUESTION:
        flash('曲が少なくて作れません')
        return render_template('games/start.html')

    else:
        # 正解を作る(id)
        correct = []
        for i in range(MAX_QUESTION):
            while True:
                index = random.randint(1, songs_count)
                if index not in correct:
                    correct.append(index)
                    break
        # 選択肢を作成(id)
        select = [[0 for i in range(4)] for j in range(10)]
        for i in range(MAX_QUESTION):
            select[i][random.randint(0, MAX_SELECT - 1)] = correct[i]
            for j in range(MAX_SELECT):
                if select[i][j] == 0:
                    while True:
                        index = random.randint(1, songs_count)
                        if index not in select[i]:
                            select[i][j] = index
                            break

        # track_idで問題作る

        records = {}
        song_correct = []
        song_select = []
        for i in range(MAX_QUESTION):
            song = Song.query.filter(Song.id == correct[i]).first()
            records["question" + str(i + 1) + "_correct_track_id"] = song.track_id
            song = SongSchema().dump(song)
            song_correct.append(song)

            for j in range(MAX_SELECT):
                song = Song.query.filter(Song.id == select[i][j]).first()
                records["question" + str(i + 1) + "_select" + str(j + 1) + "_track_id"] = song.track_id
                song = SongSchema().dump(song)
                song_select.append(song)

        this_game = Game(**records)
        db.session.add(this_game)
        db.session.commit()

        # print(song_correct)
        session.pop('correct', None)
        print(session)
        session['question'] = 1
        session['answer'] = []
        session['judge'] = []
        session['gameid'] = this_game.id
        session['select'] = song_select
        # session['correct'] = song_correct

        flash('新しくゲームが作成されました')
        return redirect(url_for('question'))


@app.route('/game/question')
def question():
    print(session)
    print('question')
    correct = session['correct']
    select = session['select']
    gameid = session['gameid']
    question = session['question']
    answer = session['answer']
    judge = session['judge']

    return render_template('games/start.html')

#
# # song登録画面
# @app.route('/admin/song', methods=['POST'])
# # @login_required
# def add_song():
#     term = request.form['term']
#     limit = request.form['limit']
#     attribute = request.form['attribute']
#
#     # api接続
#     ITUNES_URI = 'https://itunes.apple.com/search'
#
#     params = {
#         'media': 'music',
#         'country': 'jp',
#         'lang': 'ja_jp',
#         'term': term,
#         'limit': limit,
#         'attribute': attribute
#     }
#
#     if attribute == 'all':
#         params.pop('attribute')
#
#     res = requests.get(ITUNES_URI, params)
#     _status_code = res.status_code
#     _json = res.json()
#
#     if _status_code == 200:
#         track_ids = []
#         for result in _json['results']:
#             track_ids.append(result['trackId'])
#
#         duplicate = Song.query.with_entities(Song.track_id).filter(Song.track_id.in_(track_ids)).all()
#         dup_track_id = []
#         for dup in duplicate:
#             dup_track_id.append(dup[0])
#         print('duplicateTrackId: ', dup_track_id)
#
#         items = []
#         for result in _json['results']:
#             if result['trackId'] not in dup_track_id:
#                 dt = result['releaseDate']
#                 dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))
#
#                 item = Song(
#                     track=result['trackName'],
#                     track_id=result['trackId'],
#                     artist=result['artistName'],
#                     artist_id=result['artistId'],
#                     genre=result['primaryGenreName'],
#                     jacket_img=result['artworkUrl100'],
#                     preview=result['previewUrl'],
#                     release_date=dt
#                 )
#                 items.append(item)
#
#         db.session.add_all(items)
#         db.session.commit()
#
#         flash('新曲が登録されました')
#
#     else:
#         flash('楽曲の取得に失敗しました・・')
#         print('status code: ', _status_code)
#
#     return redirect('/admin/song')
