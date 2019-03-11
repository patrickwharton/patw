from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                validators = [DataRequired()])
    password = PasswordField("Password",
                validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

class LogInForm(FlaskForm):
    email = StringField("Email",
                validators = [DataRequired()])
    password = PasswordField("Password",
                validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class UploadForm(FlaskForm):
    file = FileField("Select File", validators = [DataRequired()])
    map_name = StringField("Optional: Name Your Map", validators = [Length(min=2, max=20)])
    submit = SubmitField("Create Map!")
