# 00 - Descrevendo o projeto
'''
1º [Linha 06] - Importando a função find_packages do módulo setuptools - A função find_packages() encontra diretórios
automaticamente (Pacotes Python Aplicação e seus arquivos), sem precisar digitar.
'''

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
