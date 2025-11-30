# Documentação: `simulando_dados.py`

## Objetivo

Este script é um utilitário poderoso para **configuração e teste** do projeto. Sua principal função é gerar automaticamente todos os arquivos de entrada (`.json`, `.csv`, `.txt`) necessários para que os outros scripts funcionem corretamente.

Ele cria dados fictícios (simulados) para alunos, cursos, disciplinas e notas, permitindo que você teste todo o fluxo de automação sem precisar de dados reais.

**Use este script para:**
*   Configurar o ambiente do projeto pela primeira vez.
*   Restaurar os arquivos de dados para um estado padrão.
*   Realizar testes nas ferramentas gráficas e scripts de linha de comando.

## Como Usar

1.  **Execute o script** a partir do terminal na raiz do projeto:
    ```bash
    python simulando_dados.py
    ```
2.  **Confirmação**: O script pedirá uma confirmação antes de prosseguir, pois ele **sobrescreverá** arquivos existentes. Digite `s` e pressione Enter para continuar.
3.  **Verificação**: Após a execução, verifique as pastas `inputs` e `output` para ver os arquivos gerados.

## Arquivos Gerados

O script criará (ou sobrescreverá) os seguintes arquivos e pastas:

### Na pasta `inputs/`:
*   `map_disciplinas.json`: O arquivo de configuração central com a estrutura de cursos, prefixos e disciplinas.
*   `relatorio_consolidado.csv`: Um relatório de notas fictício com dados para os cursos técnicos.
*   `turma_ds_base.txt` e `turma_pj_base.txt`: Listas mestras de alunos para os cursos técnicos.

### Na pasta `inputs/ef/`:
*   `turma_ef9a_base.txt`, `turma_ef8a_base.txt`, etc.: Listas mestras para as turmas do Ensino Fundamental.

### Na pasta `output/`:
*   O script também simula a execução dos scripts de processamento para gerar alguns arquivos de exemplo, como `ds_Administracao_de_Banco_de_Dados.txt`, `pj_Game_Design.txt` e `ef9a_t1_Computacao.txt`, deixando o ambiente pronto para teste.

## Importante

*   **Sobrescrita de Arquivos**: Tenha cuidado ao executar este script, pois ele **substituirá** os arquivos de dados existentes nas pastas `inputs` e `output`.
*   **Dados Fictícios**: Todos os nomes, RAs e notas são gerados aleatoriamente e não representam informações reais.