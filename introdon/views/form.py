from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, Regexp


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


class SettingForm(FlaskForm):
    age_list = [
        (1960, '1960'),
        (1970, '1970'),
        (1980, '1980'),
        (1990, '1990'),
        (2000, '2000'),
        (2010, '2010'),
        (2020, '2020'),
    ]
    age_first = [(1900, '指定しない')]
    age_last = [(2100, '指定しない')]
    placeholder = {"placeholder": "指定しない"}

    artist = StringField('アーティスト', render_kw=placeholder)
    genre = StringField('ジャンル', render_kw=placeholder)
    release_from = SelectField('ここから', default=1900, choices=age_first + age_list)
    release_end = SelectField('ここまで', default=2100, choices=age_list + age_last)
