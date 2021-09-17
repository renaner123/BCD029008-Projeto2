import threading
import time

from flask import Flask, flash, redirect, url_for, request, session, render_template, jsonify
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, timedelta, date


# https://fontawesome.com/icons
from flask_fontawesome import FontAwesome

# Salvando senhas de maneira apropriada no banco de dados.
# https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security
# Para gerar a senha a ser salva no DB, faça:
# senha = generate_password_hash('1234')
from werkzeug.security import generate_password_hash, check_password_hash

from forms.login import LoginForm
from forms.contato import ContatoForm
from forms.emprestimo import EmprestimoForm
from forms.efetuarEmprestimo import EfetuarEmprestimoForm
from forms.renovarEmprestimo import RenovarEmprestimoForm
from forms.finalizarEmprestimo import FinalizarEmprestimoForm

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/projeto2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Usuario = Base.classes.usuario
# Contato = Base.classes.contato
# Telefone = Base.classes.telefone
EmprestimosDB = Base.classes.Emprestimo
Aluno = Base.classes.Alunos
EquipamentoDB = Base.classes.Equipamento
SemestreDB = Base.classes.Semestre
AtividadeDB = Base.classes.Atividade
KitDB = Base.classes.Kit

boostrap = Bootstrap(app)
fa = FontAwesome(app)

nav = Nav()
nav.init_app(app)


@nav.navigation()
def meunavbar():
    menu = Navbar('Sistema de empréstimos')
    menu.items = [View('Inicial', 'inicio'), ]
    menu.items.append(Subgroup('Emprestimos', View('Efetuar emprestimo', 'efetuar_emprestimo'),
                               View('Renovar emprestimos', 'renovar_emprestimo'),
                               View('Finalizar emprestimos', 'finalizar_emprestimo')))
    menu.items.append(Subgroup('Relatórios', View('Emprestimos ativos', 'listar_emprestimos')))
    menu.items.append(View('Sair', 'logout'))
    return menu


@app.route('/login', methods=['GET', 'POST'])
def autenticar():
    if session.get('logged_in'):
        return redirect(url_for('inicio'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = db.session.query(Usuario).filter(Usuario.username == form.username.data).first()
        if usuario:
            if check_password_hash(usuario.password, form.password.data):
                session['logged_in'] = True
                session['nome'] = usuario.nome
                session['idUsuario'] = usuario.idUsuario
                return redirect(url_for('inicio'))
        flash('Usuário ou senha inválidos')
        return redirect(url_for('autenticar'))
    return render_template('login.html', title='Autenticação de usuários', form=form)


@app.route('/')
def inicio():
    if not session.get('logged_in'):
        return redirect(url_for('autenticar'))
    else:
        return render_template('index.html', title='Inicial', usuario=session.get('nome'))


@app.route("/logout")
def logout():
    '''
    Para encerrar a sessão autenticada de um usuário
    :return: redireciona para a página inicial
    '''
    session.clear()
    return redirect(url_for('inicio'))


@app.errorhandler(404)
def page_not_found(e):
    '''
    Para tratar erros de páginas não encontradas - HTTP 404
    :param e:
    :return:
    '''
    return render_template('404.html'), 404


@app.route('/emprestimo/efetuar', methods=['GET', 'POST'])
def efetuar_emprestimo():
    if session.get('logged_in'):
        form = EfetuarEmprestimoForm()
        if form.validate_on_submit():
            matricula = request.form['matricula']
            idEquipamento = request.form['idEquipamento']
            idAtividade = request.form['idAtividade']
            if (db.session.query(Aluno).filter_by(matricula=matricula).first() is not None and
                    (db.session.query(KitDB).filter_by(idKit=idEquipamento).first() is not None or
                     db.session.query(EquipamentoDB).filter_by(idEquipamento=idEquipamento).first() is not None)):
                auxAluno = db.session.query(Aluno).filter_by(matricula=matricula).first()

                if (db.session.query(AtividadeDB).filter_by(idAtividade=int(idAtividade)).first() is None):
                    flash(f"Atividade {idAtividade} é inválida", category="danger")
                    return redirect(url_for('autenticar'))
                if (auxAluno.temEmprestimo == 1):
                    flash(f"Aluno {auxAluno.matricula} já possui emprestimo", category="danger")
                    return redirect(url_for('autenticar'))
                if (auxAluno.penalidade != None):
                    flash(f"Aluno {auxAluno.matricula} possui {auxAluno.penalidade} dias de penalidade",
                          category="danger")
                    return redirect(url_for('autenticar'))
                if (auxAluno.situacao == 0):
                    flash(f"Aluno {auxAluno.matricula} não está ativo no curso", category="danger")
                    return redirect(url_for('autenticar'))

                newEmprestimo = criarEmprestimo(matricula, idAtividade, idEquipamento)
                auxAluno.temEmprestimo = 1

                db.session.add(newEmprestimo)
                db.session.commit()
                flash(f"Emprestimo do equipamento {idEquipamento} realizado", category="success")
            else:
                flash(f"Equipamento {idEquipamento} ou aluno {matricula} não existe no banco ", category="danger")

            return redirect(url_for('autenticar'))
    return render_template('efetuar_emprestimo.html', title='Efetuar emprestimo', form=form)


@app.route('/emprestimo/renovar', methods=['GET', 'POST'])
def renovar_emprestimo():
    if session.get('logged_in'):
        form = RenovarEmprestimoForm()
        if form.validate_on_submit() or request.form.to_dict() != {}:
            matricula = request.form['matricula']
            idEmprestimo = request.form['idEmprestimo']

            if (db.session.query(EmprestimosDB).filter(EmprestimosDB.idEmprestimo == idEmprestimo).first() is not None):
                auxEmprestimo = db.session.query(EmprestimosDB).filter(EmprestimosDB.idEmprestimo == idEmprestimo).first()

                if (int(auxEmprestimo.matricula) == int(matricula)):
                    auxAluno = db.session.query(Aluno).filter_by(matricula=auxEmprestimo.matricula).first()
                    if (auxAluno.situacao == 1):
                        pass
                    else:
                        flash(f"Aluno {auxAluno.matricula} não está ativo no curso", category="danger")
                        return redirect(url_for('autenticar'))
                    if (auxEmprestimo.quantidadeEmprestimo < 3):
                        pass
                    else:
                        flash(f"Emprestimo {idEmprestimo} já foi renovado 3 vezes", category="danger")
                        return redirect(url_for('autenticar'))
                    if ((datetime.now() < auxEmprestimo.dataDevolucao)):
                        pass
                    else:
                        flash(f"Emprestimo {idEmprestimo} já venceu, não pode renovar", category="danger")
                        return redirect(url_for('autenticar'))
                    auxEmprestimo.quantidadeEmprestimo = auxEmprestimo.quantidadeEmprestimo + 1
                    if (int(auxEmprestimo.idAtividade) == 500):
                        dataDevolucao = datetime.now() + timedelta(days=15)
                    else:
                        semestre = db.session.query(SemestreDB).filter_by(idSemestre=1).first()
                        dataDevolucao = semestre.ultimoDiaLetivo
                    auxEmprestimo.dataDevolucao = dataDevolucao
                    db.session.commit()
                    flash(f"Emprestimo {idEmprestimo} renovado", category="success")
                    return redirect(url_for('autenticar'))
                flash(f"Aluno {int(matricula)} não é dono do emprestimo {auxEmprestimo.idEmprestimo}", category="danger")
                return redirect(url_for('autenticar'))

            flash(f"Emprestimo {idEmprestimo} não existe", category="danger")
            return redirect(url_for('autenticar'))
    return render_template('renovar_emprestimo.html', title='Renovar emprestimo', form=form)


@app.route('/emprestimo/finalizar', methods=['GET', 'POST'])
def finalizar_emprestimo():
    if session.get('logged_in'):
        form = FinalizarEmprestimoForm()
        if form.validate_on_submit() or request.form.to_dict() != {}:
            idEmprestimo = request.form['idEmprestimo']
            if (db.session.query(EmprestimosDB).filter(EmprestimosDB.idEmprestimo == idEmprestimo).first() is not None):
                auxEmprestimo = db.session.query(EmprestimosDB).filter(EmprestimosDB.idEmprestimo == idEmprestimo).first()
                auxAluno = db.session.query(Aluno).filter_by(matricula=auxEmprestimo.matricula).first()
                if(datetime.now() > auxEmprestimo.dataDevolucao):
                    auxAluno.penalidade = (datetime.now()-auxEmprestimo.dataDevolucao).days

                if (auxAluno.temEmprestimo == 0):
                    flash(f"Aluno {auxAluno.nome} não tem emprestimo", category="danger")
                    return redirect(url_for('autenticar'))
                else:
                    auxEmprestimo.dataEntrega = datetime.now()
                    auxAluno.temEmprestimo = 0
                    flash(f"Emprestimo {idEmprestimo} finalizado", category="success")
                    db.session.commit()
                    return redirect(url_for('autenticar'))

            flash(f"Emprestimo {idEmprestimo} inválido", category="danger")
            return redirect(url_for('autenticar'))
    return render_template('finalizar_emprestimo.html', title='Finalizar emprestimo', form=form), 200


@app.route('/emprestimo',methods=['GET', 'POST'])
def listar_emprestimos():
    if session.get('logged_in'):
        form = EmprestimoForm()
        emprestimos = db.session.query(EmprestimosDB).filter(EmprestimosDB.dataEntrega == None)
        return render_template('emprestimo_listar.html', emprestimos=emprestimos, form=form)
    return redirect(url_for('autenticar'))

def criarEmprestimo(matricula, idAtividade, idEquipamento):
    dataAgora = datetime.now()
    if (int(idAtividade) == 500):
        dataDevolucao = dataAgora + timedelta(days=15)
    else:
        semestre = db.session.query(SemestreDB).filter_by(idSemestre=1).first()
        dataDevolucao = semestre.ultimoDiaLetivo

    emprestimoToCrate = EmprestimosDB(dataSaida=dataAgora,
                                      dataDevolucao=dataDevolucao,
                                      quantidadeEmprestimo=1,
                                      matricula=matricula,
                                      idAtividade=idAtividade,
                                      idEquipamentoEmprestado=idEquipamento)

    return emprestimoToCrate


def difDatas(data1, data2):
    if (data2 > data1):
        return abs((data1 - data2).days)
    else:
        return abs((data1 - data2).days) - 1


@app.route('/hello', methods=['GET'])
def helloWorld():
    print("Hello")
    return ("Hello")


class Emprestimo(db.Model):
    idEmprestimo = db.Column(db.Integer(), primary_key=True)
    dataSaida = db.Column(db.DateTime, nullable=False)
    dataEntrega = db.Column(db.DateTime, nullable=True)
    dataDevolucao = db.Column(db.DateTime, nullable=False)
    quantidadeEmprestimo = db.Column(db.Integer, nullable=False)
    matricula = db.Column(db.Integer, nullable=False)
    idAtividade = db.Column(db.Integer, nullable=False)
    idEquipamentoEmprestado = db.Column(db.Integer, nullable=False)



if __name__ == '__main__':
    app.run(debug=True)
