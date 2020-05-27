from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from introdon import app, db
from introdon.models.users import User
from introdon.views.form import UserForm


@app.route('/', methods=['GET', 'POST'])
def index():
    # ログイン済み
    if current_user.is_authenticated:
        return redirect(url_for('entrance'))

    # ユーザーログイン
    form = UserForm()
    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('entrance'))

        else:
            flash('登録が見当たりません。確認の上、再度ログインしてください。')

    return render_template('users/index.html', form=form)


@app.route('/user/new', methods=['GET', 'POST'])
def create_user():
    # ユーザー新規作成
    form = UserForm()

    if form.validate_on_submit() and request.method == 'POST':
        username = form.username.data
        password = form.password.data

        user = User(
            username=username,
            password=generate_password_hash(password, method='sha256')
        )

        duplicateCode = 1062
        try:
            db.session.add(user)
            db.session.commit()

            login_user(user)

            flash('登録されました! Welcome "{}"!!'.format(current_user.username))
            return redirect(url_for('entrance'))

        except Exception as e:
            print(e)
            if e.orig.args[0] == duplicateCode:
                flash('そのユーザー名はすでに使用されてます。')
            else:
                flash('ユーザー登録でエラーが発生しました。')

    return render_template('users/new.html', form=form)


@app.route('/user/entrance')
@login_required
def entrance():
    user = User.query.filter(User.id == current_user.id).first()

    user = {
        'name': user.username,
        'sum_game': user.sum_game,
        'sum_answer': user.sum_answer,
        'sum_correct': user.sum_correct,
        'rate': user.rate,
        'sum_score': user.sum_score
    }

    return render_template('users/entrance.html', user=user)


@app.route('/logout')
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('index'))
