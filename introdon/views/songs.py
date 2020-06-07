from flask import request, redirect, flash

from introdon import app
from introdon.models.songs import Song


# song登録画面
@app.route('/admin/song', methods=['POST'])
def add_song():
    term = request.form['term']
    limit = request.form['limit']
    attribute = request.form['attribute']

    validate, _status_code = Song.add_song(term, attribute, limit)

    if validate:
        flash('新曲が登録されました')
    else:
        flash('楽曲の取得に失敗しました・・')
        print('status code: ', _status_code)

    return redirect('/admin/song')
