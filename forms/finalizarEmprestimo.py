from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField, validators, IntegerField

class FinalizarEmprestimoForm(FlaskForm):
    idEmprestimo = IntegerField('idEmprestimo',[validators.DataRequired()])
    btnAtualizar = SubmitField('Confirmar')
