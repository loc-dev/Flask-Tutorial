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
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
