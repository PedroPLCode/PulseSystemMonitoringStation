from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Optional

class UserForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional()])
    is_admin = BooleanField('Administrator')
    email_alerts_receiver = BooleanField('Odbiorca alertów email')
    telegram_alerts_receiver = BooleanField('Odbiorca alertów Telegram')
    telegram_chat_id = StringField('Telegram Chat ID', validators=[Optional()])
    date_created = DateTimeField('Data utworzenia', validators=[Optional()])
    last_login = DateTimeField('Ostatnie logowanie', validators=[Optional()])
