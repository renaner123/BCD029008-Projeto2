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
#Contato = Base.classes.contato
#Telefone = Base.classes.telefone
Emprestimo = Base.classes.emprestimo
Aluno = Base.classes.alunos
Equipamento = Base.classes.equipamento
Kit = Base.classes.kit


#Equipamento_has_Emprestimo = Base.classes.equipamento_has_emprestimo
#Kit_has_Emprestimo = Base.classes.kit_has_emprestimo

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

            flash(f"Emprestimo do equipamento {idEquipamento} realizado", category="success")

            return redirect(url_for('autenticar'))

    return render_template('efetuar_emprestimo.html', title='Efetuar emprestimo', form=form)

@app.route('/emprestimo/renovar', methods=['GET', 'POST'])
def renovar_emprestimo():
    if session.get('logged_in'):
        form = RenovarEmprestimoForm()
        if form.validate_on_submit():
            matricula = request.form['matricula']
            idEmprestimo = request.form['idEmprestimo']
            print(matricula, idEmprestimo)
            return redirect(url_for('autenticar'))
    return render_template('renovar_emprestimo.html', title='Renovar emprestimo', form=form)


@app.route('/emprestimo/finalizar', methods=['GET', 'POST'])
def finalizar_emprestimo():
    if session.get('logged_in'):
        form = FinalizarEmprestimoForm()
        if form.validate_on_submit():
            idEmprestimo = request.form['idEmprestimo']
            print(idEmprestimo)
            return redirect(url_for('autenticar'))
    return render_template('finalizar_emprestimo.html', title='Finalizar emprestimo', form=form)


@app.route('/emprestimo')
def listar_emprestimos():
    if session.get('logged_in'):
        form = EmprestimoForm()
        emprestimos = db.session.query(Emprestimo)
        return render_template('emprestimo_listar.html', emprestimos=emprestimos, form=form)
    return redirect(url_for('autenticar'))


#@app.route('/contato', methods=['POST'])
# def dados_contato():
#     if session.get('logged_in'):
#         id_usuario = session.get('idUsuario')
#         id_contato = int(request.form['id'])
#
#         # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#common-filter-operators
#         contato = db.session.query(Contato).filter(Contato.idUsuario == id_usuario,
#                                                    Contato.idContato == id_contato).first()
#
#         contado_dict = dict()
#
#         contado_dict['id'] = contato.idContato
#         contado_dict['nome'] = contato.nome
#         contado_dict['dataNasc'] = contato.dataNasc.strftime('%d/%m/%Y')
#
#         return jsonify(contado_dict)
#
#     return redirect(url_for('autenticar'))


# @app.route('/atualizarcontato', methods=['POST'])
# def atualizar_contato():
#     if session.get('logged_in'):
#         id_usuario = session.get('idUsuario')
#         id_contato = request.form['idContato']
#         nome = request.form['nome']
#         dataNasc = request.form['dataNasc']
#
#         contato = db.session.query(Contato).filter(Contato.idUsuario == id_usuario,
#                                                    Contato.idContato == id_contato).first()
#
#         contato.nome = nome
#         abc = datetime.strptime(dataNasc, '%d/%m/%Y').date()
#         contato.dataNasc = abc.strftime('%Y-%m-%d')
#
#         db.session.commit()
#
#         return redirect(url_for('autenticar'))
#
#     return redirect(url_for('autenticar'))

if __name__ == '__main__':
    app.run(debug=True)
