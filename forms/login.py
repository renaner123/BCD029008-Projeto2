from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, validators

class LoginForm(FlaskForm):
    username = StringField('Login',[validators.DataRequired()])
    password = PasswordField('Senha', [validators.DataRequired()])
    submit = SubmitField('Entrar')
