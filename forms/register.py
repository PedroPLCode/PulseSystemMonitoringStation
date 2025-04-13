from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    recaptcha = RecaptchaField()
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    email = StringField(
        render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        render_kw={"placeholder": "Confirm password"},
        validators=[DataRequired(), EqualTo("password")],
    )
    submit = SubmitField("Register")
