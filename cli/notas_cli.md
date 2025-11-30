# Documentação: Ferramenta de Linha de Comando (`notas`)

## Objetivo

O projeto inclui uma ferramenta de linha de comando (CLI) chamada `notas` para fornecer acesso rápido a funcionalidades comuns diretamente do seu terminal. Isso permite realizar tarefas, como consultas rápidas, sem a necessidade de abrir as interfaces gráficas.

A ferramenta é construída usando o arquivo `cli/notas_cli.py` e é tornada "instalável" através do arquivo `setup.py`.

## Instalação

Para que o comando `notas` funcione em qualquer pasta do seu terminal, você precisa "instalar" o projeto em modo de desenvolvimento.

1.  **Abra o terminal** na pasta raiz do projeto (a pasta que contém o `setup.py`).
2.  **Execute o seguinte comando**:
    ```bash
    pip install -e .
    ```

*   **O que este comando faz?** Ele usa o `setup.py` para criar um link simbólico para o seu projeto no ambiente Python. A parte mais importante é que ele cria o executável `notas` e o adiciona automaticamente ao PATH do sistema.
*   A flag `-e` (editável) significa que qualquer alteração que você fizer no código (por exemplo, adicionar um novo comando em `notas_cli.py`) será refletida instantaneamente, sem a necessidade de reinstalar.

## Comandos Disponíveis

### `notas ra`

Encontra o RA de um aluno procurando em todos os arquivos de lista mestra (`*_base.txt`) dentro das pastas `inputs/` e `inputs/ef/`.

#### Como Usar

```bash
notas ra <parte_do_nome_do_aluno>
```

#### Exemplo

```bash
notas ra antonio
```