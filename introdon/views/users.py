from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Regexp

from introdon import app, db
from introdon.models.logs import Log
from introdon.models.users import User


class UserForm(FlaskForm):
    # 半角英数のみ
    message_reg = '半角英数のみでお願いします。'
    message_len = '4文字以上10文字以内でお願いします。'

    username = StringField('ユーザーネーム', validators=[InputRequired('A username is required!'),
                                                  Regexp("^[a-zA-Z0-9]+$", message=message_reg),
                                                  Length(min=4, max=10, message=message_len)])
    password = PasswordField('パスワード', validators=[InputRequired('A password is required!'),
                                                  Regexp("^[a-zA-Z0-9]+$", message=message_reg),
                                                  Length(min=4, max=10, message=message_len)])


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
            flash('Please check your login details and try again.')

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
    # logからquery
    log = Log.query.filter(Log.user_id == current_user.id).all()
    sum_answer = len(log)
    sum_correct = [value.judge for value in log].count(1)
    sum_game = [value.question_num for value in log].count(10)
    total_score = sum([value.score for value in log])

    try:
        rate = round(sum_correct / sum_answer, 2)
    except Exception as e:
        rate = 0

    user = {
        'name': current_user.username,
        'sum_game': sum_game,
        'sum_answer': sum_answer,
        'sum_correct': sum_correct,
        'rate': rate,
        'total_score': total_score
    }

    # user成績を更新
    update_user = User.query.filter(User.id == current_user.id).first()
    update_user.sum_game = sum_game
    update_user.sum_answer = sum_answer
    update_user.sum_correct = sum_correct
    update_user.rate = rate
    db.session.add(update_user)
    db.session.commit()

    return render_template('users/entrance.html', user=user)


@app.route('/logout')
def logout():
    logout_user()
    flash('ログアウトしました')
    return redirect(url_for('index'))
