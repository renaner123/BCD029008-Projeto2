from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField, HiddenField, validators

class ContatoForm(FlaskForm):
    idContato = HiddenField('idContato')
    nome = StringField('Nome',[validators.DataRequired()])
    dataNasc = DateField('Data de nascimento',[validators.DataRequired()],format='%d/%m/%Y')
    btnAtualizar = SubmitField('Confirmar')
