from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})


class RutrackerPage(FlaskForm):
    # url = StringField('url торрента', validators=[DataRequired()])
    submit = SubmitField('Вход')


class RutrackerSearch(FlaskForm):
    search_text = StringField('Текст для поиска', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Искать', render_kw={"class": "btn btn-primary"})
