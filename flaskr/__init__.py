# 01 - Estabelecendo a nossa Fábrica de Aplicativos,
# qualquer configuração ou registro precisa acontecer aqui dentro da função.
'''
1º [Linha 09] - Importando o módulo os - Possibilidade do código em Python interagir com o sistema operacional
2º [Linha 11] - Importando a classe Flask do módulo flask
3º [Linha 14 até 24] - Definindo a função 'create_app', a nossa Fábrica de Aplicativos
'''

import os

from flask import Flask

# Definição das configurações para o aplicativo Flaskr.
def create_app(test_config=None):
    # O parâmetro (instance_relative_config=Bool), Informa para o Flaskr,
    # que os arquivos de configurações confidenciais são relativos à pasta de instância.
    # Essa pasta de instância, será localizada fora do pacote flaskr, é definida no seguinte local padrão (/instance)
    app = Flask(__name__, instance_relative_config=True)
    # O 'Config', se comporta como dicionário regular, oferecendo carregamento de configurações para o Flaskr,
    # com o método (.from_mapping), atualiza as configurações de carregamento do 'Config'.
    # O 'SECRET_KEY' é uma chave de configuração, utilizada para manter os dados seguros, tanto o Flask e as extensões,
    # vão utilizar a chave, por padrão seu valor é None. Mas, durante o desenvolvimento da aplicação,
    # utilizar um valor em String, em implatanção, use valor aleatório sendo convertido em bytes.
    # O 'DATABASE', usa o método .join() que une um ou mais componentes de caminho forma inteligente,
    # logo, este caminho a ser configurado é onde o arquivo de banco de dados SQLite será salvo.
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Nessa condição, se o parâmetro [test_config] houver definido para sí, o seu valor None (Nenhum),
    # as configuraçaões para o Flaskr, será carregada com novas configurações de um arquivo Python,
    # através do método (.from_pyfile), caso existir esse arquivo 'config.py', quando não estiver testando,
    # outro parâmetro [silent] aceita valores bool, no caso com o valor True definido, se o arquivo 'config.py'
    # estiver ausente, haverá uma falha, porém, silenciosa.
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Essa condição só será feita, onde o parâmetro [test_config], estiver com um arquivo de configuração
        # definido na pasta de instância,logo, será carregado com novas informações do arquivo, através do método
        # (.from_mapping).
        app.config.from_mapping(test_config)

    # Tratamento de exceções - Certifique-se de que Pasta de Instância existe
    # Primeiro, é executado a cláusula try (Tente Fazer), será criado Pasta de Instância fora do pacote flaskr
    # Caso ocorrer tudo certo, o bloco de except será ignorado.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Estabelecendo um decorador route(), para visualizar o aplicativo funcionando com a função definida no Python
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    return app
