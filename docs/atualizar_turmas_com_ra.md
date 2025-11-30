# Documentação: `atualizar_turmas_com_ra.py`

## Objetivo

**Este script é exclusivo para as turmas técnicas (ex: Desenvolvimento de Sistemas, Programação de Jogos).**

Sua função é gerar ou atualizar as listas de alunos (`turma_*.txt`) com os RAs corretos e as notas mais recentes, que são lidas do arquivo `relatorio_consolidado.csv`.

O script utiliza o arquivo `map_disciplinas.json` como fonte de configuração, permitindo que novas turmas sejam adicionadas sem a necessidade de alterar o código.

## Como Usar

1.  **Preparar os Arquivos de Entrada**:
    *   Para cada turma que você deseja atualizar, copie a lista de alunos (com nome e "Código RA") do sistema acadêmico.
    *   Cole essa lista em um arquivo de texto dentro da pasta `inputs/`. O nome do arquivo deve corresponder ao que está configurado na chave `site_list` em `map_disciplinas.json` (ex: `ds_seduc_site.txt`, `pj_seduc_site.txt`).

2.  **Executar o Script**:
    ```bash
    python atualizar_turmas_com_ra.py
    ```

3.  **Menu Interativo**:
    *   O script exibirá um menu com todas as turmas configuradas.
    *   Você pode escolher atualizar uma turma específica, todas de uma vez, ou sair.

## Entradas (Arquivos Necessários)

*   **`inputs/map_disciplinas.json`**: Essencial. O script lê este arquivo para obter as configurações de cada turma técnica, incluindo:
    *   `site_list`: O nome do arquivo de texto de entrada (ex: `"ds_seduc_site.txt"`).
    *   `output_file`: O nome do arquivo de texto de saída (ex: `"turma_ds.txt"`).
    *   `nome_completo`: O nome do curso como aparece no CSV.
*   **`inputs/<nome_do_arquivo_site_list>.txt`**: Um arquivo de texto para cada turma, contendo a lista de alunos copiada do site.
*   **`inputs/relatorio_consolidado.csv`**: O arquivo CSV com as notas consolidadas de onde as notas serão extraídas.

## Saídas (Arquivos Gerados)

*   **`turma_*.txt`**: Para cada turma processada, um arquivo de texto é gerado na raiz do projeto (conforme a chave `output_file` no JSON). Este arquivo contém a lista de alunos na ordem correta, com RAs e notas, pronto para ser usado como uma "lista mestra" (`turma_*_base.txt`) pelo `mapear_notas.py`.

## Uso Prático

Após gerar um arquivo `turma_*.txt`, você pode renomeá-lo para `turma_*_base.txt` e movê-lo para a pasta `inputs/` para usá-lo como a lista mestra definitiva no script `mapear_notas.py`.