from flask import redirect, url_for, flash
from flask_admin import Admin, expose, AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_login import LoginManager, current_user

from introdon import app, db
from introdon.models.games import Game
from introdon.models.logs import Log
from introdon.models.songs import Song
from introdon.models.users import User

# flask_login設定
login_manager = LoginManager()
login_manager.init_app(app)

# login_viewのrouteを設定
# login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# 管理画面
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class MyModelView(ModelView):
    column_display_pk = True
    page_size = 50
    # CSRF対策
    form_base_class = SecureForm

    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.admin
        else:
            return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))


class SongModelView(MyModelView):
    column_searchable_list = ['artist', 'track']
    column_default_sort = ('id', True)

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        return_url = "../"
        return self.render('admin/create_song.html', return_url=return_url)


class UserModelView(MyModelView):
    column_default_sort = ('id', True)
    form_edit_rules = ('username', 'admin')
    can_create = False
    column_exclude_list = ('password')
    column_searchable_list = ['username']


class IntroLinkView(BaseView):
    @expose('/')
    def intro_link(self):
        return redirect(url_for('index'))


admin = Admin(app, template_mode='bootstrap3', index_view=MyAdminIndexView())
admin.add_view(SongModelView(Song, db.session))
admin.add_view(MyModelView(Game, db.session))
admin.add_view(MyModelView(Log, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(
    IntroLinkView(name='IntroDon', endpoint='introdon', menu_icon_type='glyph', menu_icon_value='glyphicon-home'))


@app.errorhandler(404)
def not_exist_route(error):
    flash('Page not found')
    return redirect(url_for('index'))


@app.errorhandler(401)
def unauthorized_error(error):
    flash('Unauthorized error')
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_server_error(error):
    flash('Internal server error')
    return redirect(url_for('index'))
