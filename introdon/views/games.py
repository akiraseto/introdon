import random
from datetime import datetime
from datetime import timedelta

import requests
from flask import redirect, url_for, render_template, flash, session, request
from flask_login import current_user, login_required

from introdon import app, db
from introdon.models.games import Game
from introdon.models.logs import Log
from introdon.models.songs import Song, SongSchema
from introdon.models.users import User

MAX_QUESTION = 10
MAX_SELECT = 4
START_WAITING_TIME = 20
DISPLAY_TIME = 2
QUESTION_TIME = 10
ANSWER_TIME = 7


@app.route('/game/setting_multi')
@login_required
def setting_multi():
    # 1人目:gameRecord作成 2人目以降:gameRecordをupdateしてstart_multiにredirect
    latest_game = Game.query.order_by(Game.id.desc()).first()
    session['creatable'] = True

    # game_idで受付中のものがある場合(createから数秒以内で、参加人数に空きあり)
    if latest_game != None and timedelta(
            seconds=START_WAITING_TIME) > datetime.now() - latest_game.created_at and not latest_game.entry_user5:
        # 自分idのエントリーが無かったら、
        if current_user.id not in [latest_game.entry_user1, latest_game.entry_user2, latest_game.entry_user3,
                                   latest_game.entry_user4]:

            # gameにユーザー追加する
            for i in range(1, 6):
                if not getattr(latest_game, 'entry_user' + str(i)):
                    setattr(latest_game, 'entry_user' + str(i), current_user.id)
                    break

            latest_game.modified_at = datetime.now()
            db.session.add(latest_game)
            db.session.commit()

        # session['id'](game.id) から correct_id、select_idを作成
        correct_id = []
        select_id = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]

        for i in range(MAX_QUESTION):
            attr_name = "question" + str(i + 1) + "_correct_song_id"
            id = getattr(latest_game, attr_name)
            correct_id.append(id)

            for j in range(MAX_SELECT):
                attr_name = "question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"
                id = getattr(latest_game, attr_name)
                select_id[i][j] = id

        session['id'] = latest_game.id
        session['correct'] = correct_id
        session['select'] = select_id
        session['created_timestamp'] = datetime.timestamp(latest_game.created_at)
        session['creatable'] = False

        # start_multiにリダイレクト
        return redirect(url_for('start_multi'))

    return render_template('games/setting_multi.html')


@app.route('/game/start_multi', methods=['POST', 'GET'])
@login_required
def start_multi():
    # 1人目ならgameを作る
    if session['creatable']:

        # 曲の絞り込み機能
        artist = request.form['artist']
        genre = request.form['genre']
        release_from = request.form['release_from']
        release_end = request.form['release_end']

        release_from = datetime.strptime(release_from, '%Y')
        release_end = datetime.strptime(release_end, '%Y')

        # 曲を追加したかチェック
        no_add_song = 0
        while no_add_song < 2:

            song_instance = Song.query.with_entities(Song.id).filter(Song.artist.like('%' + artist + '%'),
                                                                     Song.genre.like('%' + genre + '%'),
                                                                     Song.release_date >= release_from,
                                                                     Song.release_date < release_end).all()
            song_instance = [value[0] for value in song_instance]

            # gameをgenerateしてDBに保存する
            # レコード数をカウント
            songs_count = len(song_instance)

            if songs_count >= MAX_QUESTION * 4:
                break

            # 登録曲が少なすぎる場合
            if no_add_song < 1:

                ITUNES_URI = 'https://itunes.apple.com/search'

                # termを作る
                term = ''
                if artist and genre:
                    term = artist + "+" + genre
                elif artist and not genre:
                    term = artist
                elif not artist and genre:
                    term = genre

                params = {
                    'media': 'music',
                    'country': 'jp',
                    'lang': 'ja_jp',
                    'term': term,
                    'limit': 50
                }

                res = requests.get(ITUNES_URI, params)
                _status_code = res.status_code
                _json = res.json()

                if _status_code == 200:
                    # すでに曲が登録している場合は省く
                    track_ids = []
                    for result in _json['results']:
                        track_ids.append(result['trackId'])

                    duplicate = Song.query.with_entities(Song.track_id).filter(Song.track_id.in_(track_ids)).all()
                    dup_track_id = []
                    for dup in duplicate:
                        dup_track_id.append(dup[0])
                    print('duplicateTrackId: ', dup_track_id)

                    items = []
                    for result in _json['results']:
                        if result['trackId'] not in dup_track_id:
                            dt = result['releaseDate']
                            dt = datetime.fromisoformat(dt.replace('Z', '+00:00'))

                            item = Song(
                                track=result['trackName'],
                                track_id=result['trackId'],
                                artist=result['artistName'],
                                artist_id=result['artistId'],
                                genre=result['primaryGenreName'],
                                jacket_img=result['artworkUrl100'],
                                preview=result['previewUrl'],
                                release_date=dt
                            )
                            items.append(item)

                    db.session.add_all(items)
                    db.session.commit()

                no_add_song += 1
            else:
                break

        # 登録曲が少なすぎる場合
        if songs_count < MAX_QUESTION * 4:

            flash('該当曲が少なくて問題を作れません、範囲を広めてください。')
            return render_template('games/setting_multi.html')

        else:
            # 正解を作る
            correct_id = []
            for i in range(MAX_QUESTION):
                while True:
                    index = random.randint(0, songs_count - 1)
                    if index not in correct_id:
                        correct_id.append(index)
                        break
            correct_id = [song_instance[i] for i in correct_id]

            # 選択肢を作成
            select_id = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]

            for i in range(MAX_QUESTION):
                rand_index = random.randint(0, MAX_SELECT - 1)
                select_id[i][rand_index] = correct_id[i]
                for j in range(MAX_SELECT):
                    if select_id[i][j] == 0:
                        while True:
                            index = song_instance[random.randint(0, songs_count - 1)]
                            if index not in select_id[i]:
                                select_id[i][j] = index

                                break

            # song_idにしてGame tableに保存
            records = {}
            for i in range(MAX_QUESTION):
                records["question" + str(i + 1) + "_correct_song_id"] = correct_id[i]
                for j in range(MAX_SELECT):
                    records["question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"] = select_id[i][j]

            records["entry_user1"] = current_user.id

            this_game = Game(**records)
            db.session.add(this_game)
            db.session.commit()

            session['id'] = this_game.id
            session['correct'] = correct_id
            session['select'] = select_id
            session['created_timestamp'] = datetime.timestamp(this_game.created_at)
            session['creatable'] = False

    session['num'] = 1
    session['answer'] = []
    session['judge'] = []
    session['correct_song'] = {}

    game = {
        'limit_time': round(session['created_timestamp'] + START_WAITING_TIME),
        'DISPLAY_TIME': DISPLAY_TIME,
        'game_id': session['id']
    }

    return render_template('games/start_multi.html', game=game)


@app.route('/game/question_multi')
@login_required
def question_multi():
    # 参加が1人なら、ゲーム不成立。
    chk_entry = Game.query.with_entities(Game.entry_user2).filter(Game.id == session['id']).all()
    if not chk_entry[0][0]:
        return redirect(url_for('failure_multi'))

    # 10問やってるなら、resultに送る
    if session['num'] > MAX_QUESTION:
        return redirect(url_for('result_multi'))

    num = session['num']
    correct = session['correct']
    select = session['select']

    song = Song.query.filter(Song.id == correct[num - 1]).first()
    session['correct_song'] = SongSchema().dump(song)

    game = {
        'num': session['num'],
        'correct_song': session['correct_song'],
        'select_song': Song.query.filter(Song.id.in_(select[num - 1])).all(),
        'limit_time': round(
            session['created_timestamp'] + START_WAITING_TIME + QUESTION_TIME * num + ANSWER_TIME * (num - 1)),
        'DISPLAY_TIME': DISPLAY_TIME,
    }

    return render_template('games/question_multi.html', game=game)


@app.route('/game/record_log_multi', methods=['POST'])
@login_required
def record_log_multi():
    num = session['num']
    answer = int(request.form['answer'])
    session['answer'].append(answer)
    correct = session['correct'][num - 1]

    judge = 0
    if answer == correct:
        judge = 1
    session['judge'].append(judge)

    # Logにinsert
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None

    # scoreをlogに追加する
    score = 0
    if answer == correct:
        log_count = Log.query.filter(Log.game_id == session['id'], Log.question_num == num).count()

        if log_count == 0:
            score = 50
        elif log_count == 1:
            score = 40
        elif log_count == 2:
            score = 30
        elif log_count == 3:
            score = 20
        else:
            score = 10

    log = Log(
        user_id=user_id,
        game_id=session['id'],
        select_song_id=answer,
        judge=judge,
        score=score,
        question_num=num,
        correct_song_id=correct
    )
    db.session.add(log)
    db.session.commit()

    session['num'] += 1
    return redirect(url_for('answer_multi'))


@app.route('/game/answer_multi')
@login_required
def answer_multi():
    game = {
        'num': session['num'] - 1,
        'judge': session['judge'][-1],
        'correct_song': session['correct_song'],
        'limit_time': round(
            session['created_timestamp'] + START_WAITING_TIME + (QUESTION_TIME + ANSWER_TIME) * (session['num'] - 1)),
        'DISPLAY_TIME': DISPLAY_TIME,
    }

    return render_template('games/answer_multi.html', game=game)


@app.route('/game/result_multi')
@login_required
def result_multi():
    # 結果内容
    correct_song_list = Song.query.filter(Song.id.in_(session['correct'])).all()
    correct_song_list = [next(s for s in correct_song_list if s.id == id) for id in session['correct']]

    # Logを集計してGameのgold_user...bronze_scoreをupdateする
    # Gameから参加ユーザーのidを取得する
    game_users = []
    game_instance = Game.query.filter(Game.id == session['id']).first()
    for i in range(1, 6):
        attr_name = "entry_user" + str(i)
        user_id = getattr(game_instance, attr_name)
        if user_id != None:
            game_users.append(user_id)

    # dictで合計得点を集める{user_id: sum_score}
    score_dict = {}
    for game_user in game_users:
        score_dict[game_user] = 0

    # 取得した参加user_idごとに得点を計算
    log_records = Log.query.filter(Log.game_id == session['id']).all()
    for record in log_records:
        if record.user_id in game_users:
            score_dict[record.user_id] += record.score

    order_score = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

    # Gameのgold_user...bronze_scoreをupdateする
    grade_name = ['gold_user', 'silver_user', 'bronze_user']
    grade_score = ['gold_score', 'silver_score', 'bronze_score']

    for i, j in enumerate(order_score):
        setattr(game_instance, grade_name[i], j[0])
        setattr(game_instance, grade_score[i], j[1])

    game_instance.modified_at = datetime.now()
    db.session.add(game_instance)
    db.session.commit()

    # ユーザー名と正解数を一致させる
    # Userから参加ユーザーの名前を取得
    user_id_name = User.query.with_entities(User.id, User.username).filter(User.id.in_(game_users)).order_by(
        User.id).all()
    display_rank = {name: value for id, name in user_id_name for id2, value in score_dict.items() if id == id2}
    display_rank = sorted(display_rank.items(), key=lambda x: x[1], reverse=True)

    game = {
        'judge': session['judge'],
        'correct_song_list': correct_song_list,
        'count_judge': session['judge'].count(1),
        'display_rank': display_rank
    }

    return render_template('games/result_multi.html', game=game)


@app.route('/game/failure_multi')
@login_required
def failure_multi():
    return render_template('games/failure_multi.html')


@app.route('/game/setting')
def setting_game():
    return render_template('games/setting.html')


@app.route('/game/start', methods=['POST'])
def start_game():
    # 曲の絞り込み機能
    artist = request.form['artist']
    artist = '%' + artist + '%'
    genre = request.form['genre']
    genre = '%' + genre + '%'
    release_from = request.form['release_from']
    release_end = request.form['release_end']

    release_from = datetime.strptime(release_from, '%Y')
    release_end = datetime.strptime(release_end, '%Y')

    song_instance = Song.query.with_entities(Song.id, Song.track_id).filter(Song.artist.like(artist),
                                                                            Song.genre.like(genre),
                                                                            Song.release_date >= release_from,
                                                                            Song.release_date < release_end).all()

    # gameをgenerateしてDBに保存する
    # レコード数をカウント
    songs_count = len(song_instance)

    # 登録曲が少なすぎる場合
    if songs_count < MAX_QUESTION * 4:
        flash('該当曲が少なくて問題を作れません、範囲を広めてください。')
        return render_template('games/setting.html')

    else:
        # 正解を作る(id)
        correct = []
        for i in range(MAX_QUESTION):
            while True:
                index = random.randint(0, songs_count - 1)
                if index not in correct:
                    correct.append(index)
                    break
        correct = [song_instance[i] for i in correct]
        correct_id = [value[0] for value in correct]

        # 選択肢を作成(id)
        select = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]
        select_id = [[0 for i in range(MAX_SELECT)] for j in range(MAX_QUESTION)]

        for i in range(MAX_QUESTION):
            rand_index = random.randint(0, MAX_SELECT - 1)
            select[i][rand_index] = correct[i]
            select_id[i][rand_index] = correct[i][0]
            for j in range(MAX_SELECT):
                if select[i][j] == 0:
                    while True:
                        index = song_instance[random.randint(0, songs_count - 1)]
                        if index not in select[i]:
                            select[i][j] = index
                            select_id[i][j] = index[0]

                            break

        # song_idにしてGame tableに保存
        records = {}
        for i in range(MAX_QUESTION):
            records["question" + str(i + 1) + "_correct_song_id"] = correct[i][1]
            for j in range(MAX_SELECT):
                records["question" + str(i + 1) + "_select" + str(j + 1) + "_song_id"] = select[i][j][1]

        if current_user.is_authenticated:
            records["entry_user1"] = current_user.id

        this_game = Game(**records)
        db.session.add(this_game)
        db.session.commit()

        session['num'] = 1
        session['answer'] = []
        session['judge'] = []
        session['id'] = this_game.id
        session['correct'] = correct_id
        session['select'] = select_id
        session['correct_song'] = {}

        session['created_timestamp'] = None

        return redirect(url_for('question'))


@app.route('/game/question')
def question():
    # 10問やってるなら、resultに送る
    if session['num'] > MAX_QUESTION:
        return redirect(url_for('result'))

    num = session['num']
    correct = session['correct']
    select = session['select']

    song = Song.query.filter(Song.id == correct[num - 1]).first()
    session['correct_song'] = SongSchema().dump(song)

    game = {
        'num': session['num'],
        'correct_song': session['correct_song'],
        'select_song': Song.query.filter(Song.id.in_(select[num - 1])).all()
    }

    return render_template('games/question.html', game=game)


@app.route('/game/record_log', methods=['POST'])
def record_log():
    num = session['num']
    answer = int(request.form['answer'])
    session['answer'].append(answer)
    correct = session['correct'][num - 1]

    judge = 0
    if answer == correct:
        judge = 1
    session['judge'].append(judge)

    # Logにinsert
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None

    # scoreをlogに追加する
    score = 0
    if answer == correct:
        score = 10

    log = Log(
        user_id=user_id,
        game_id=session['id'],
        select_song_id=answer,
        judge=judge,
        score=score,
        question_num=num,
        correct_song_id=correct
    )
    db.session.add(log)
    db.session.commit()

    session['num'] += 1
    return redirect(url_for('answer'))


@app.route('/game/answer')
def answer():
    game = {
        'num': session['num'] - 1,
        'judge': session['judge'][-1],
        'correct_song': session['correct_song'],
    }

    return render_template('games/answer.html', game=game)


@app.route('/game/result')
def result():
    # 結果内容
    correct_song_list = Song.query.filter(Song.id.in_(session['correct'])).all()
    correct_song_list = [next(s for s in correct_song_list if s.id == id) for id in session['correct']]

    game = {
        'judge': session['judge'],
        'correct_song_list': correct_song_list,
        'count_judge': session['judge'].count(1)
    }

    return render_template('games/result.html', game=game)
