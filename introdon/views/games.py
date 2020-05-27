from datetime import datetime
from datetime import timedelta

from flask import redirect, url_for, render_template, session, request
from flask_login import current_user, login_required

from introdon import app
from introdon.models.games import Game, GameLogic
from introdon.models.logs import LogLogic
from introdon.models.songs import SongLogic
from introdon.models.users import UserLogic
from introdon.views.config_introdon import *
from introdon.views.form import SettingForm


@app.route('/game/setting_multi')
@login_required
def setting_multi():
    # 1人目:gameを新規作成 2人目以降はアップデートしてstart_multiにリダイレクト
    session['creatable'] = True
    form = SettingForm()
    user_id = current_user.id

    latest_game = Game.query.order_by(Game.id.desc()).first()
    entry_list = [latest_game.entry_user1, latest_game.entry_user2, latest_game.entry_user3, latest_game.entry_user4,
                  latest_game.entry_user5]

    # game_idで受付中のものがある場合(createから数秒以内で、参加人数に空きあり)
    if latest_game != None and timedelta(
            seconds=START_WAITING_TIME) > datetime.now() - latest_game.created_at and not entry_list[-1]:
        game_logic = GameLogic()

        # 自分idのエントリーが無かったら、
        if user_id not in entry_list:
            # gameにユーザーを追加
            game_logic.participate_in_game(latest_game, user_id)

        # game_idからcorrect_id、select_idを取得
        correct_id, select_id = game_logic.fetch_songs_id(latest_game)

        session['id'] = latest_game.id
        session['correct'] = correct_id
        session['select'] = select_id
        session['created_timestamp'] = datetime.timestamp(latest_game.created_at)
        session['creatable'] = False

        # start_multiにリダイレクト
        return redirect(url_for('start_multi'))

    return render_template('games/setting_multi.html', form=form)


@app.route('/game/start_multi', methods=['POST', 'GET'])
@login_required
def start_multi():
    # 1人目ならgameを作る
    if session['creatable']:
        form = SettingForm()
        artist = form.artist.data
        genre = form.genre.data
        release_from = form.release_from.data
        release_end = form.release_end.data
        user_id = current_user.id

        song_logic = SongLogic()
        validate_make_q = None
        flash = ''
        correct_id = []
        select_id = []

        # 1度ループ 曲チェック=>追加のため
        count_loop = 0
        while count_loop < 2:
            # クイズを作る
            validate_make_q, flash, correct_id, select_id = song_logic.make_question(artist, genre, release_from,
                                                                                     release_end)

            # クイズを作れた場合
            if validate_make_q:
                break

            # クイズを作れない場合
            # ループ 初回
            if count_loop < 1:
                term = ''
                if artist and genre:
                    term = artist + "+" + genre
                elif artist and not genre:
                    term = artist
                elif not artist and genre:
                    term = genre

                # itunesからDBに曲追加
                song_logic.add_song(term)
                count_loop += 1

            # ループ済みなら抜ける
            else:
                break

        # ループ後
        # クイズが作れなかった場合
        if not validate_make_q:
            flash(flash)
            return render_template('games/setting_multi.html', form=form)

        else:
            game_logic = GameLogic()
            game_id, game_created_at = game_logic.create_game(correct_id, select_id, user_id)

            session['id'] = game_id
            session['correct'] = correct_id
            session['select'] = select_id
            session['created_timestamp'] = datetime.timestamp(game_created_at)
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
    selects = session['select']

    # クイズ用の曲をシリアライズして用意する
    song_logic = SongLogic()
    correct_song, select_songs = song_logic.dump_question_song(correct, selects, num)

    session['correct_song'] = correct_song
    game = {
        'num': session['num'],
        'correct_song': correct_song,
        'select_song': select_songs,
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
    correct = session['correct'][num - 1]
    game_id = session['id']
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id

    log_logic = LogLogic()
    judge = log_logic.create_log(user_id, game_id, num, correct, answer, is_multi=True)

    session['answer'].append(answer)
    session['judge'].append(judge)
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
    correct_songs = session['correct']
    game_id = session['id']
    game_instance = Game.query.filter(Game.id == game_id).first()

    # 正解曲の内容を出力
    song_logic = SongLogic()
    correct_song_list = song_logic.dump_correct_songs_list(correct_songs)

    # 参加したuserのidを取得
    game_logic = GameLogic()
    users_id_list = game_logic.fetch_users_id(game_instance)

    # ユーザーごとの得点を集計
    log_logic = LogLogic()
    order_score = log_logic.calc_score(game_id, users_id_list)

    # 発表用にユーザー名と得点を対応させる
    user_logic = UserLogic()
    display_rank = user_logic.bind_name_score(users_id_list, order_score)

    # Gameのゴールド、シルバー、ブロンズ内容をupdate
    game_logic.update_game(order_score, game_instance)

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


@app.route('/game/setting', methods=['GET', 'POST'])
def setting_game():
    form = SettingForm()
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id

    if request.method != 'POST':
        return render_template('games/setting.html', form=form)

    else:
        artist = form.artist.data
        genre = form.genre.data
        release_from = form.release_from.data
        release_end = form.release_end.data

        song_logic = SongLogic()
        validate_make_q, flash, correct_id, select_id = song_logic.make_question(artist, genre, release_from,
                                                                                 release_end)

        if validate_make_q:
            game_logic = GameLogic()
            game_id, game_created_at = game_logic.create_game(correct_id, select_id, user_id)

            session['num'] = 1
            session['answer'] = []
            session['judge'] = []
            session['id'] = game_id
            session['correct'] = correct_id
            session['select'] = select_id
            session['correct_song'] = {}
            session['created_timestamp'] = None
        else:
            flash(flash)
            return render_template('games/setting.html', form=form)

        return redirect(url_for('question'))


@app.route('/game/question')
def question():
    # 10問やってるなら、resultに送る
    if session['num'] > MAX_QUESTION:
        return redirect(url_for('result'))

    num = session['num']
    correct = session['correct']
    selects = session['select']

    # クイズ用の曲をシリアライズして用意する
    song_logic = SongLogic()
    correct_song, select_songs = song_logic.dump_question_song(correct, selects, num)

    session['correct_song'] = correct_song
    game = {
        'num': session['num'],
        'correct_song': correct_song,
        'select_song': select_songs
    }

    return render_template('games/question.html', game=game)


@app.route('/game/record_log', methods=['POST'])
def record_log():
    # todo: ユーザースコア計算をLog追加ごとに変更
    num = session['num']
    answer = int(request.form['answer'])
    correct = session['correct'][num - 1]
    game_id = session['id']
    user_id = None
    if current_user.is_authenticated:
        user_id = current_user.id

    log_logic = LogLogic()
    judge, score = log_logic.create_log(user_id, game_id, num, correct, answer)

    # UserDBにスコアをupdate
    user_logic = UserLogic()
    user_logic.add_score_to_user(user_id, score)

    session['answer'].append(answer)
    session['judge'].append(judge)
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
    # 正解曲の内容をダンプ
    correct_songs = session['correct']
    song_logic = SongLogic()
    correct_song_list = song_logic.dump_correct_songs_list(correct_songs)

    game = {
        'judge': session['judge'],
        'correct_song_list': correct_song_list,
        'count_judge': session['judge'].count(1)
    }

    return render_template('games/result.html', game=game)
