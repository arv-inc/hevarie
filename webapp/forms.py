from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RutrackerPage(FlaskForm):
    # url = StringField('url торрента', validators=[DataRequired()])
    submit = SubmitField('Вход')


class RutrackerSearch(FlaskForm):
    search_text = StringField('Текст для поиска', validators=[DataRequired()])
    submit = SubmitField('Искать')
