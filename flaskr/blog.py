# 04 - Criando o Blueprint de Blog
'''
1º [Linha 10] - Importando a função abort do módulo werkzeug (Dependência do Flask) - Essa função
abort, é uma exceção especial que retorna um código de status HTTP com uma mensagem opcional
para mostrar qual foi o erro.
'''

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

# Criando o nome do Blueprint com 'blog',
# marcando a sua localização com o segundo argumento, usamos __name__.
bp = Blueprint('blog', __name__)

# Nesta visualização de índice principal da página, será apresentado todas as postagens,
# as mais recentes terão como destaque em primeiro.
@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

# A visualização da função 'create' é parecida com 'register' do Blueprint de autenticação,
# se os dados validados para a postagem estão corretos será adicionados ao banco de dados,
# senão, um erro será apresentado.
# Agora teremos o decorador login_required usado para exigir autenticação em algumas visualizações.
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)"
                " VALUES (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

# Essa função 'get_post', evita a duplicidade de código, iremos verificar se uma determinada postagem no blog
# é do autor que corresponde ao usuário conectado, e,
# assim podemos chamar essa função para visualização a função 'update' e 'delete'.
def get_post(id, check_author=True):
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

# Nossa próxima visualização a função 'update',
# o usuário que no caso deve ser o autor conseguirá editar sua postagem no aplicativo flaskr.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ?"
                " WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

# Por fim, temos a última visualização a função 'delete', que permite o usuário a excluir uma postagem.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
