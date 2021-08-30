from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField, validators, IntegerField

class RenovarEmprestimoForm(FlaskForm):
    idEmprestimo = IntegerField('idEmprestimo')
    matricula = IntegerField('matricula',[validators.DataRequired()])
    btnAtualizar = SubmitField('Confirmar')