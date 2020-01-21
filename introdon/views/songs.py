from flask import render_template

from introdon import app
from introdon.models.songs import Song


@app.route('/songs')
# @login_required
def show_songs():
    songs = Song.query.order_by(Song.id.desc()).all()
    return render_template('songs/index.html', songs=songs)

# @app.route('/songs', methods=['POST'])
# # @login_required
# def add_song():
#     entry = Entry(
#         title=request.form['title'],
#         text=request.form['text']
#     )
#     db.session.add(entry)
#     db.session.commit()
#     flash('新しく記事が作成されました')
#     return redirect(url_for('show_songs'))
#
#
# @app.route('/songs/new', methods=['GET'])
# # @login_required
# def new_song():
#     return render_template('songs/new.html')

#
# @app.route('/entries/<int:id>', methods=['GET'])
# @login_required
# def show_entry(id):
#     entry = Entry.query.get(id)
#     return render_template('entries/show.html', entry=entry)
#
#
# @app.route('/entries/<int:id>/edit', methods=['GET'])
# @login_required
# def edit_entry(id):
#     entry = Entry.query.get(id)
#     return render_template('entries/edit.html', entry=entry)
#
#
# @app.route('/entries/<int:id>/update', methods=['POST'])
# @login_required
# def update_entry(id):
#     entry = Entry.query.get(id)
#     entry.title = request.form['title']
#     entry.text = request.form['text']
#     db.session.merge(entry)
#     db.session.commit()
#     flash('記事が更新されました')
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/entries/<int:id>/delete', methods=['POST'])
# @login_required
# def delete_entry(id):
#     entry = Entry.query.get(id)
#     db.session.delete(entry)
#     db.session.commit()
#     flash('投稿が削除されました')
#     return redirect(url_for('show_entries'))
