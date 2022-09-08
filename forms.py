import os

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, NumberRange, EqualTo


class LoginForm(FlaskForm):
    username = StringField("Benutzername", validators=[DataRequired()])
    password = PasswordField("Passwort", validators=[DataRequired()])
    submit = SubmitField("Login")

class AdminRegisterForm(FlaskForm):
    username = StringField("Benutzername", validators=[DataRequired(message="*erforderlich")])
    user_email = StringField("E-Mail-Adresse", validators=[DataRequired(message="*erforderlich")])
    password = PasswordField("Passwort", validators=[DataRequired(message="*erforderlich")])
    confirm_password = PasswordField("Passwort bestätigen", validators=[DataRequired(message="*erforderlich"), EqualTo("password", message="Das Passwort stimmt nicht überein.")])
    rights = SelectField("Rechte", choices=["user", "admin"], validators=[DataRequired()])
    submit = SubmitField("Registrieren")

class RegisterForm(FlaskForm):
    username = StringField("Benutzername", validators=[DataRequired(message="*erforderlich")])
    user_email = StringField("E-Mail-Adresse", validators=[DataRequired(message="*erforderlich")])
    password = PasswordField("Passwort", validators=[DataRequired(message="*erforderlich")])
    confirm_password = PasswordField("Passwort bestätigen", validators=[DataRequired(message="*erforderlich"), EqualTo("password", message="Das Passwort stimmt nicht überein.")])
    submit = SubmitField("Registrieren")