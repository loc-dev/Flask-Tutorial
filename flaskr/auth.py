# 03 - Criando o Blueprint de Autenticação
'''
1º [Linha 07] - Importando o módulo functools - Fornece recursos como funções,
para trabalhar em outras funções e objetos que podem ser chamados
'''

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Criando o nome do Blueprint com 'auth', no segundo argumento, usamos __name__,
# agora o Blueprint saberá onde está definido. Depois, o último argumento url_prefix,
# podemos usar subdomínio de URL associados ao Blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Aqui será a nossa primeira visualização a função 'register', o usuário poderá registrar no aplicativo flaskr,
# para isso a URL especificada será um conjunto da url_prefix: '/auth' + o decorador route()
# da Blueprint '/register'.
@bp.route('/register', methods=('GET', 'POST'))
def register():
    # Se o usuário preencheu os dados ao formulário e confirmou, o método 'POST',
    # encarrega-se de enviar os dados recebidos para o servidor.
    if request.method == 'POST':
        # Começamos a validar as seguintes entradas preenchidas pelo usuário,
        # através do request.form, é um tipo de Dicionário [dict],
        # podemos mapear os campos do formulário (chaves para dicionário)
        username = request.form['username']
        password = request.form['password']
        # Chamando a função 'get_db', sendo aplicada na variável db
        db = get_db()
        # Na variável error, estamos declarando o valor None
        error = None

        # Condições para username e password
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # Na validação não houve nenhum erro, portanto,
        # os novos dados inseridos pelo usuário serão passados para o Banco de Dados.
        # Em db.execute(), o método .execute(), está enviando a sintaxe SQL com espaços reservados (?)
        # de qualquer entrada do usuário, será escapado os valores para não ocorrer uma ataque de injeção de SQL.
        # Com o generate_password_hash(), podemos usar em questão de segurança nas senhas declaradas passando em hash,
        # nunca devemos armazená-las as senhas diretamente no banco de dados.
        # Toda modificação realizada ao Banco de dados  devemos usar o método .commit(), para salvar as alterações.
        # A exceção .IntegrityError, ocorrerá caso o nome do usuário (username) já existir.
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f'User {username} is already registered.'
            else:
                # Após o armazenamento de dados do usuário, deve ser redirecionado para a página de login,
                # com a função 'url_for' que gera uma URL dinamicamente com base nome do usuário.
                # A função 'redirect', retornar uma resposta de redirecionamento para aquela função 'url_for'.
                return redirect(url_for("auth.login"))
        # Caso houver falhas, o método flask(), a mensagem que está sendo carregada são de erros,
        # logo, podem ser recuperadas durante a renderização do Template.
        flash(error)

    return render_template('auth/register.html')

# Nossa próxima visualização a função 'login', onde o usuário consegue acessar o aplicativo flaskr.
# A URL especificada será um conjunto da url_prefix: '/auth' + o decorador route() da Blueprint '/login'.
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        # Iremos validar novamente as seguintes entradas preenchidas pelo usuário.
        username = request.form['username']
        password = request.form['password']
        # Chamando a função 'get_db', sendo aplicada na variável db
        db = get_db()
        # Na variável error, estamos declarando o valor None
        error = None
        # Com o método .execute(), realizamos a consulta (query) através da sintaxe SQL.
        # O método .fetchone(), retorna uma única sequência de consulta ou None, quando não há dados disponíveis.
        # O método .fetchall(), será usado, pois, retorna uma lista de todas as linhas (restantes)
        # de um resultado de consulta (query).
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        # Condições para username e password
        if user is None:
            error = 'Incorrect username.'
        # Validando a senha preenchida atualmente em Hashes, com o hash armazenado no Banco de Dados.
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # O objeto da classe Flask, conhecido como 'Session',
            # é um dicionário [Dict] onde são armazenados os dados de solicitações.
            # Caso todas as validações sejam bem-sucedida, o user com seu ['id'] é armazenado em uma nova session,
            # essa session serão armazenados em um Cookie sendo enviado ao navegador,
            # onde envia de volta com solicitações subsequentes.
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

