import random

from flask import redirect, url_for, render_template, flash, session, request

from introdon import app, db
from introdon.models.games import Game
from introdon.models.logs import Log
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
        return render_template('games/index.html')

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
        # todo:iteratorでall取得に直すqueryは1回で済む
        for i in range(MAX_QUESTION):
            song = Song.query.filter(Song.id == correct[i]).first()
            records["question" + str(i + 1) + "_correct_track_id"] = song.track_id

            for j in range(MAX_SELECT):
                song = Song.query.filter(Song.id == select[i][j]).first()
                records["question" + str(i + 1) + "_select" + str(j + 1) + "_track_id"] = song.track_id

        this_game = Game(**records)
        db.session.add(this_game)
        db.session.commit()

        session['num'] = 1
        session['answer'] = []
        session['judge'] = []
        session['id'] = this_game.id
        session['correct'] = correct
        session['select'] = select
        session['correct_song'] = {}

        # flash('新しくゲームが作成されました')
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


@app.route('/game/answer', methods=['POST'])
def answer():
    # todo:リダイレクトで問題ナンバーが進んでしまうので直す
    num = session['num']
    answer = int(request.form['answer'])
    session['answer'].append(answer)
    correct = session['correct'][num - 1]

    judge = 0
    if answer == correct:
        judge = 1
    session['judge'].append(judge)

    # logテーブルにinsertする(logは個人成績集計&発表で後々使用)
    log = Log(
        game_id=session['id'],
        select_song_id=answer,
        judge=judge,
        question_num=num,
        correct_song_id=correct
    )
    db.session.add(log)
    db.session.commit()

    game = {
        'num': num,
        'judge': judge,
        'correct_song': session['correct_song'],
    }

    session['num'] += 1
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
