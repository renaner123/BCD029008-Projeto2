from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField, validators, IntegerField

class EfetuarEmprestimoForm(FlaskForm):
    idEmprestimo = HiddenField('idEmprestimo')
    matricula = IntegerField('matricula',[validators.DataRequired()])
    idEquipamento = IntegerField('idEquipamento',[validators.DataRequired()])
    btnAtualizar = SubmitField('Confirmar')
