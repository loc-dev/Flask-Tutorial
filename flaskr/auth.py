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


