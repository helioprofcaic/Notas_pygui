# Documentação: Ferramenta de Linha de Comando (`notas`)

## Objetivo

O projeto inclui uma ferramenta de linha de comando (CLI) chamada `notas` para fornecer acesso rápido a funcionalidades comuns diretamente do seu terminal. Isso permite realizar tarefas, como consultas rápidas, sem a necessidade de abrir as interfaces gráficas.

A ferramenta é construída usando o arquivo `cli/notas_cli.py` e é tornada "instalável" através do arquivo `setup.py`.

## Instalação (Duas Opções)

### Opção 1: Usando um Arquivo de Lote (Recomendado para Windows)

Este método permite que o comando `notas` funcione de qualquer lugar, **ativando automaticamente o ambiente virtual (`.venv`) do projeto**.

1.  **Crie o arquivo `notas.bat`**: Na pasta raiz do projeto (`b:\Dev\Notas_pygui\`), crie um arquivo chamado `notas.bat` com o seguinte conteúdo:
    ```batch
    @echo off
    REM Executa o script usando o Python do ambiente virtual do projeto.
    "%~dp0.venv\Scripts\python.exe" "%~dp0cli\notas_cli.py" %*
    ```
2.  **Adicione a Pasta ao PATH do Sistema**:
    *   Pesquise por "Editar as variáveis de ambiente do sistema" no menu Iniciar.
    *   Clique em "Variáveis de Ambiente...".
    *   Na seção "Variáveis do sistema", encontre e selecione a variável `Path` e clique em "Editar".
    *   Clique em "Novo" e adicione o caminho completo para a pasta raiz do seu projeto (ex: `B:\Dev\Notas_pygui`).
    *   Clique "OK" em todas as janelas.
3.  **Reinicie o Terminal**: Feche e abra uma nova janela do terminal. Agora o comando `notas` estará disponível globalmente.

### Opção 2: Usando `pip install` (Tradicional)

Este método instala o comando, mas **requer que você ative o ambiente virtual manualmente** (`.\.venv\Scripts\activate`) toda vez que for usá-lo.

1.  **Abra o terminal** na pasta raiz do projeto.
2.  **Garanta que `setuptools` está atualizado**:
    ```bash
    python -m pip install --upgrade pip setuptools wheel
    ```
3.  **Execute o comando de instalação**:
    ```bash
    pip install -e .
    ```

## Comandos Disponíveis

### Obtendo Ajuda

Você pode obter ajuda para qualquer comando adicionando a flag `--help` ao final dele.

```bash
# Ajuda para o comando principal (lista todos os sub-comandos)
notas --help

# Ajuda para o sub-comando 'ra'
notas ra --help

# Ajuda para o sub-comando 'atualizar'
notas atualizar --help
```

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