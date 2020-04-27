from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RutrackerPage(FlaskForm):
    submit = SubmitField('Вход')


class RutrackerSearch(FlaskForm):
    search_text = StringField(
        'Текст для поиска', validators=[DataRequired()],
        render_kw={"class": "form-control mr-sm-2", "type": "search", "placeholder": "Введите текст для поиска"}
        )
    submit = SubmitField('Искать', render_kw={"class": "btn btn-outline-success my-2 my-sm-0"})
