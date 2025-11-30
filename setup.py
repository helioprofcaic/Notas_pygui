# setup.py

# Este arquivo é usado para transformar o projeto em um pacote Python instalável.
# Com ele, você pode instalar a ferramenta CLI no seu ambiente Python usando pip,
# e o pip cuidará de criar o comando 'notas' e torná-lo acessível globalmente no terminal.
#
# Para usar:
# 1. Navegue até a pasta raiz do projeto (a pasta que contém este arquivo).
# 2. Execute `pip install -e .` no terminal.
#    O `-e` (editável) instala o pacote de uma forma que as alterações no seu código
#    são refletidas imediatamente, sem precisar reinstalar.

from setuptools import setup, find_packages

setup(
    # O nome do seu pacote. É assim que ele aparecerá no `pip list`.
    name='notas-cli',

    # A versão do seu pacote.
    version='1.0.0',

    # Encontra automaticamente todos os pacotes (pastas com __init__.py) no seu projeto.
    # Isso garante que todos os seus módulos Python sejam incluídos na instalação.
    packages=find_packages(),

    # Lista de dependências que o pip instalará junto com o seu pacote.
    # Adicione aqui todas as bibliotecas que seu projeto utiliza.
    install_requires=[
        'click',    # Essencial para a criação da CLI.
        'pandas',   # Usado para manipulação de dados (ex: CSV).
        # Adicione outras dependências como 'customtkinter', 'pyautogui' se necessário.
    ],

    # O ponto de entrada (entry point) é a parte mais importante para a CLI.
    # Ele diz ao pip para criar um script executável chamado 'notas'.
    # Quando você executa 'notas' no terminal, ele chama a função 'cli'
    # que está dentro do arquivo 'notas_cli.py', no pacote 'cli'.
    entry_points='''
        [console_scripts]
        notas=cli.notas_cli:cli
    ''',
)
