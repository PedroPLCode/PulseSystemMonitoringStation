from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import re
from wtforms.validators import ValidationError


def password_complexity(form: FlaskForm, field: StringField) -> None:
    """
    Validator to enforce password complexity rules.

    Args:
        form (FlaskForm): The form instance.
        field (Field): The field containing the password data.

    Raises:
        ValidationError: If the password does not meet complexity requirements.
    """
    password = field.data
    if not re.search(r"[A-Z]", password):  # Check for uppercase letters
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):  # Check for lowercase letters
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r"[0-9]", password):  # Check for digits
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(
        r"[!@#$%^&*(),.?\":{}|<>]", password
    ):  # Check for special characters
        raise ValidationError("Password must contain at least one special character.")


class RegisterForm(FlaskForm):
    """
    A form for user registration.

    Fields:
        recaptcha (RecaptchaField): Google reCAPTCHA field for bot protection.
        username (StringField): Field for entering the username.
        email (StringField): Field for entering the email address.
        password (PasswordField): Field for entering the password.
        confirm_password (PasswordField): Field for confirming the password, must match 'password'.
        submit (SubmitField): Button to submit the registration form.
    """

    recaptcha = RecaptchaField()
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    email = StringField(
        render_kw={"placeholder": "Email"}, validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"},
        validators=[DataRequired(), Length(min=10, max=50), password_complexity],
    )
    confirm_password = PasswordField(
        render_kw={"placeholder": "Confirm password"},
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )
    submit = SubmitField("Register")
