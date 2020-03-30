from functools import wraps

from flask import request, redirect, url_for, render_template, flash, session
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

from introdon import app, db
from introdon.models.entries import Entry
from introdon.models.games import Game
from introdon.models.logs import Log
from introdon.models.songs import Song
from introdon.models.users import User

# todo:flask_loginで 管理画面に権限付与する

# flask_login設定
login_manager = LoginManager()
login_manager.init_app(app)


# login_viewのrouteを設定
# login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# todo:必ず消す
# @app.route('/login')
# def login():
#     user = User.query.filter_by(id=1).first()
#
#     login_user(user)
#
#     return redirect(url_for('secret'))
#
#
# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('index'))


# 管理画面
admin = Admin(app, template_mode='bootstrap3')


class MyModelView(ModelView):
    column_display_pk = True
    page_size = 50


class SongModelView(MyModelView):
    column_searchable_list = ['artist', 'track']
    column_default_sort = ('id', True)

    # def is_accessible(self):
    #     return True

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        return_url = "../"
        return self.render('admin/create_song.html', return_url=return_url)


admin.add_view(SongModelView(Song, db.session))
admin.add_view(MyModelView(Game, db.session))
admin.add_view(MyModelView(Log, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(ModelView(Entry, db.session))






def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return view(*args, **kwargs)

    return inner


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('ユーザ名が異なります')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('パスワードが異なります')
        else:
            session['logged_in'] = True
            flash('ログインしました')
            return redirect(url_for('show_entries'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('ログアウトしました')
    return redirect(url_for('show_entries'))


@app.errorhandler(404)
def non_existant_route(error):
    return redirect(url_for('login'))
