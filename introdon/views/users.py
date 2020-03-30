from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, current_user
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Regexp

from introdon import app, db
from introdon.models.users import User


class UserForm(FlaskForm):
    # 半角英数のみ
    message_reg = 'Must input half-width English numbers and characters'
    message_len = 'Must be between 4 and 10 characters.'

    username = StringField('username', validators=[InputRequired('A username is required!'),
                                                   Regexp("^[a-zA-Z0-9]+$", message=message_reg),
                                                   Length(min=4, max=10, message=message_len)])
    password = PasswordField('password', validators=[InputRequired('A password is required!'),
                                                     Regexp("^[a-zA-Z0-9]+$", message=message_reg),
                                                     Length(min=4, max=10, message=message_len)])


@app.route('/', methods=['GET', 'POST'])
def index():
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

            flash('Welcome "{}"!!'.format(current_user.username))
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
    # todo:成績表つくる

    print(current_user.username)
    print(current_user.sum_answer)
    print(current_user.sum_correct)
    print(current_user.rate)

    return render_template('users/entrance.html')
