# 03 - Criando o Blueprint de Autenticação
'''
1º [Linha ?] - Importando o módulo functools - Fornece recursos como funções,
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
    # encarregar de enviar os dados recebidos para o servidor.
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
        # Em db.execute(), o método .execute(), está enviando a sintaxe SQL com espaços reservados da entrada do usuário,
        # será escapado os valores para não ocorrer uma ataque de injeção de SQL.
        # Com o generate_password_hash(), podemos usar em questão de segurança nas senhas declaradas passando em hash,
        # nunca devemos armazenadas senhas diretramente no banco de dados.
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
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')
