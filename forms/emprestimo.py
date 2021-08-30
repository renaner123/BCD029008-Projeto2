from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField, HiddenField, validators, IntegerField

class EmprestimoForm(FlaskForm):
    idEmprestimo = IntegerField('idEmpretimo',[validators.DataRequired()])
    dataSaida = DateField('dataSaida',[validators.DataRequired()],format='%d/%m/%Y')
    dataEntrega = DateField('dataEntrega',[validators.DataRequired()],format='%d/%m/%Y')
    dataDevolucao = DateField('dataDevolucao',[validators.DataRequired()],format='%d/%m/%Y')
    quantidadeEmprestimo = IntegerField('quantidadeEmprestimo',[validators.DataRequired()])
    matricula = IntegerField('matricula',[validators.DataRequired()])
    idAtividade = IntegerField('idAtividade',[validators.DataRequired()])
    idEquipamentosEmprestado = IntegerField('idEquipamentosEmprestado',[validators.DataRequired()])
    btnAtualizar = SubmitField('Confirmar')