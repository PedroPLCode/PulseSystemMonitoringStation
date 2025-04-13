from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, Optional


class UserForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[Optional()])
    is_admin = BooleanField("is_admin")
    email_alerts_receiver = BooleanField("email_alerts_receiver")
    telegram_alerts_receiver = BooleanField("telegram_alerts_receiver")
    telegram_chat_id = StringField("telegram_chat_id", validators=[Optional()])
    date_created = DateTimeField("date_created", validators=[Optional()])
    last_login = DateTimeField("last_login", validators=[Optional()])
