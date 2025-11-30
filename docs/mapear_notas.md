# Documentação: `mapear_notas.py`

## Objetivo

O `mapear_notas.py` é o script central para o pré-processamento dos dados. Sua principal função é ler um relatório de notas consolidado (em formato `.csv`) e, com base em uma lista mestra de alunos, gerar arquivos de texto (`.txt`) individuais para cada disciplina de um curso.

Esses arquivos `.txt` são formatados especificamente para serem utilizados como entrada pelo script `automacao_notas.py`.

## Como Usar

1.  **Execute o script** a partir do terminal:
    ```bash
    python mapear_notas.py
    ```
2.  **Menu de Curso**: O script apresentará um menu para que você escolha o curso para o qual deseja gerar os arquivos (ex: "Técnico em Desenvolvimento de Sistemas").
3.  **Processamento**: Após a seleção, o script irá:
    *   Ler a lista de alunos do arquivo base do curso (ex: `turma_ds_base.txt`).
    *   Ler o arquivo `relatorio_consolidado.csv`.
    *   Para cada disciplina encontrada no curso, ele irá cruzar as informações e gerar um arquivo de saída na pasta `output`.

## Entradas (Arquivos Necessários)

*   **`inputs/relatorio_consolidado.csv`**: Arquivo CSV contendo as notas de todos os alunos. Deve ter as colunas: `curso`, `disciplina`, `aluno`, `av1`, `av2`, `media_final`.
*   **`output/turma_ds_base.txt`** (ou `turma_pj_base.txt`): Um arquivo de texto que serve como "lista mestra" da turma. Ele define a **ordem correta** dos alunos e garante que todos sejam incluídos no arquivo final, mesmo que não sejam encontrados no CSV (nesse caso, com notas zeradas). O formato deve ser o nome do aluno seguido pelo seu RA.

## Saídas (Arquivos Gerados)

*   **`output/ds_NOME_DA_DISCIPLINA.txt`** (ou `pj_...`): Para cada disciplina do curso escolhido, um arquivo de texto é gerado. O nome do arquivo é sanitizado (espaços viram `_`, caracteres especiais são removidos).
    *   **Conteúdo**: Cada arquivo contém blocos de texto para cada aluno, com nome, RA e as três notas (AV1, AV2, Média Final), formatados para serem lidos pelo `automacao_notas.py`.

## Funções Principais

*   `parse_master_list(filepath)`: Lê e analisa o arquivo `turma_*_base.txt` para extrair a lista de alunos e seus RAs na ordem correta.
*   `mapear_e_gerar_arquivos(...)`: Orquestra todo o processo: lê a lista mestra, lê o CSV de notas, filtra por curso, itera sobre cada disciplina e, para cada uma, gera o arquivo de saída `.txt` correspondente.
*   `sanitize_filename(name)`: Limpa o nome da disciplina para criar um nome de arquivo válido.
*   `strip_accents(text)` e `normalize_whitespace(text)`: Funções auxiliares para normalizar os nomes dos alunos, permitindo uma comparação mais robusta entre a lista mestra e o CSV.