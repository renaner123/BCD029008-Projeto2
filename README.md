## Sistema de emprestimos

### Proposta

Desenvolver uma aplicação WEB para um sistema de empréstimos de equipamentos usando Python + Flask e comunicando com banco de dados MySQL. Usando como base o [Projeto 1](https://github.com/BCD29008-classroom/2021-01-projeto-pratico-01-renaner123)

### Funcionalidades implementadas

- [x] Efetuar emprestimo
- [x] Renovar emprestimo
- [x] Finalizar emprestimo
- [x] Relatório sobre todos os empréstimos em andamento
- [x] Banco de dados MySQL.
- [x] Aplicação WEB usando Python + Flask
- [x] Modelagem do banco de dados é relacional
- [x] Conjunto de instruções DDL e DML para criar e povoar a base de dados com nome ddl-dml.sql na raiz do projeto.

### Regras de négocios implementadas
- [x] Somente alunos ativos no curso e sem débitos podem fazer empestimo;
- [x] Aluno pode fazer somente 1 emprestimo por vez;
- [x] Prazo para o empréstimo depende da atividade na qual o aluno usará o equipamento;
- [x] Ao aluno é dada a possibilidade de renovar um empréstimo somente antes do mesmo vencer
- [x] Aluno pode renovar um emprestimo por no máximo 3 vezes;
- [ ] Reserva para o emprestimo/equipamento;
- [x] Para atividades de ensino, a data de entrega, mesmo para as renovações, não deve ultrapassar o último dia letivo do semestre
- [x] Para as atividades de pesquisa,extensão e TCC o aluno poderá fazer uma renovação de forma que continue com o item emprestado durante as férias acadêmicas.



### Para executar a aplicação

O arquivo [ddl-dml.sql](ddl-dml.sql) tem as instruções DDL e DML para criar o banco. A modelagem feita com o MySQL Workbench está disponível no arquivo [modelagem.mwb](modelagem.mwb).

![diagrama ER](modelagem.png)

As configurações de acesso ao banco MySQL devem ser ajustadas no arquivo [app.py](app.py), precisamente na linha representada abaixo:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://renan:bcd1234@ampto.sj.ifsc.edu.br:33006/pp02renan'
```

O ideal é fazer uso do Python Virtualenv, mas seria possível executar a aplicação sem ele. Basta instalar os pacotes que estão no arquivo [requirements.txt.](/requirements.txt)




```shell
python3 -m venv venv
source venv/bin/activate

# para instalar os pacotes. Só é necessário fazer isso uma única vez
pip install -r requirements.txt

# para executar a aplicação
python3 app.py

```

## Para acessar a aplicação

No navegador web entre com o endereço `http://localhost:5000`. O banco conta com dois usuários para teste:

| Usuário | Senha |
| ------- | -----|
| juca    | 1234 |
| maria   | 1234 |


## Instruções para fazer emprestimos

Aqui estão alguns exemplos de emprestimos para testar as funcionalidades implementadas. As instruções que vão funcionar possui *sucesso*, as que não podem ser feitas tem *falha* nos exemplos abaixo.


* Aluno com matricula 129 não possui emprestimo e é ativo no curso. Use essa matricula e um id de atividade 500, para efetuar um emprestimo; *Sucesso*, gera data de devolução para 15 dias.
  
* Aluno com matricula 123 já possui emprestimo e está atrasado. Use essa matricula para tentar renovar o emprestimo 700; *Falha*, já passou da data de devolução.

* Emprestimo 700 está atrasado. Use essa id para finalizar o emprestimo do aluno 123; *Sucesso*. Irá gerar penalidade para o aluno.

* Aluno com matricula 123 não possui emprestimo, mas está com penalidade. Use essa matricula e um id de atividade entre(500,501 e 502) para efetuar um emprestimo; *Falha*, aluno está com penalidade.

* Aluno com matricula 128 tem emprestimo e não está atrasado. Use essa matricula para tentar renovar o emprestimo 708. Sucesso.

* Aluno com matricula 128 tem emprestimo e não está atrasado. Use essa matricula para tentar renovar o emprestimo 708. Sucesso.

* Aluno com matricula 128 tem emprestimo e não está atrasado. Use essa matricula para tentar renovar o emprestimo 708; *falha*, aluno já renovou 3 vezes esse emprestimo.

* Aluno com matricula 126 tem emprestimo e não está atrasado. Use essa matricula para finalizar o emprestimo 703; *sucesso*, aluno está em dia, não gerou penalidade.

* Aluno com matricula 127 não possui emprestimo e não é ativo no curso. Use essa matricula para tentar fazer um emprestimo; *falha*, aluno não está ativo no curso.

* Aluno com matricula 125 possui emprestimo e é ativo no curso. Use essa matricula para tentar fazer um emprestimo; *falha*, aluno já possui um emprestimo vigente

* Aluno com matricula 131 não possui emprestimo e é ativo no curso. Use essa matricula para fazer um emprestimo com id de atividade 501; *sucesso*, gera data de devolução sendo o fim do semestre.