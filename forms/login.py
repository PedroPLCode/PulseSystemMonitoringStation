from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """
    A form for user login.

    Fields:
        username (StringField): Field for entering the username.
        password (PasswordField): Field for entering the password.
        submit (SubmitField): Button to submit the form.
    """

    username: StringField = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password: PasswordField = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    submit: SubmitField = SubmitField("Login")
