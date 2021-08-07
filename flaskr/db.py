# 02 - Definindo nosso banco de dados,
# para realizar uma conexão, posteriormente, fazer consultas e operações.
'''
1º [Linha 15] - Importando o módulo sqlite3 - Fornece um Banco de Dados leve,
não requer configuração de um servidor de banco de dados
2º [Linha 17] - Importando o módulo click (Dependência do Flask) - Podemos escrever linha de comando,
permitindo adicionar aos comandos personalizados
3º [Linha 18] - Importando a função current_app do módulo flask - Essa função será utilizada para acessar dados
sobre o aplicativo em execução, incluindo a configuração | O objeto namespace 'g' - Podemos armazenar dados no
Contexto do Aplicativo durante uma solicitação ou comando CLI
4º [Linha 19] - Importando o decorador do Flask - Esse decorador, envolve um retorno de chamada para garantir que
será chamado com um Contexto de Aplicativo
'''

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# Estabelecendo a conexão com Banco de Dados, e, armazenando no objeto 'g'.
def get_db():
    # Se o atributo 'db' não for encontrado no objeto 'g',
    # será declarado um armazenamento de dados da conexão deste objeto 'g' com atributo db,
    # sendo reutilizada nas próximas solicitações.
    # Com a função '.connect()' do módulo sqlite3, podemos estabelecer a conexão com o arquivo de Banco de Dados SQLite,
    # no momento, não se encontra disponível, até que seja inicializado o Banco de Dados.
    # O 'current_app', direciona tratando da solicitação atual dada a configuração da aplicação,
    # que foi estabelecida na função 'create_app', quando a função 'get_db' for chamada,
    # o aplicativo estará processando uma solicitação, sendo assim, a função 'current_app' passa a ser usada.
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # A classe .Row do módulo sqlite3, retorna linhas em comportamento de Estrutura de Dados - Dicionário [dict],
        # permitindo acessar as colunas por nome.
        g.db.row_factory = sqlite3.Row

    return g.db

# Primeiramente a função 'close_db', irá verificar a conexão e se o atributo db foi estabelecido no objeto 'g'
def close_db(e=None):
    # Logo, se a conexão estiver estabelecida, poderá ser desconectada, também podemos usar a função 'close_db',
    # na nossa Fábrica de Aplicativos, após cada solicitação ao Banco de dados.
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Inicializando o Banco de Dados
def init_db():
    # Chamando a função 'get_db', sendo aplicada na variável db
    db = get_db()
    # Com a função '.open_resource()', podemos abrir um arquivo relativo ao Pacote flaskr
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))

# Utilizando a função 'command' estamos adicionando uma linha de comando chamado 'init-db', que chama a função 'init_db'
# Depois, temos o decorador que está envolvendo chamada a função 'init_db' garantindo dentro do Contexto de Aplicativo
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

# Registrando as seguinte funções 'close_db' e 'init_db_command' para o Aplicativo,
# o certo seria realizar a instância do aplicativo, como está indisponível, vamos escrever uma função,
# e definir no parâmetro [app] nossa variável.
def init_app(app):
    # Registrando a função assim que o Contexto de Aplicativo estiver sendo solicitado.
    app.teardown_appcontext(close_db)
    # Adicionando um novo comando juntamente com o comando flask.
    app.cli.add_command(init_db_command)
