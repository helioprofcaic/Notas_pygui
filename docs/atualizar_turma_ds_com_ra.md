# Documentação: `atualizar_turma_ds_com_ra.py`

## Objetivo

Este script foi criado para resolver um problema específico: gerar um arquivo de automação (`turma_ds.txt`) que respeita a ordem exata dos alunos e utiliza os RAs corretos, conforme exibido no sistema acadêmico.

Ele combina uma lista de alunos copiada diretamente do site (com nomes e RAs corretos) com as notas do `relatorio_consolidado.csv`. O resultado é um arquivo `turma_ds.txt` que pode ser usado como uma "lista mestra" (`turma_ds_base.txt`) mais precisa para o script `mapear_notas.py`.

## Como Usar

1.  **Copiar a Lista de Alunos**: No sistema acadêmico, copie a lista de alunos que inclui o nome completo e o "Código RA" de cada um.
2.  **Criar o Arquivo de Entrada**: Crie um arquivo de texto chamado `ds_seduc_site.txt` dentro da pasta `inputs/`.
3.  **Colar no Arquivo**: Cole a lista de alunos que você copiou dentro deste novo arquivo.
4.  **Executar o Script**:
    ```bash
    python atualizar_turma_ds_com_ra.py
    ```

## Entradas (Arquivos Necessários)

*   **`inputs/ds_seduc_site.txt`**: Um arquivo de texto contendo a lista de alunos copiada diretamente do site do sistema acadêmico. Este arquivo deve incluir o nome do aluno e, na linha seguinte, o "Código RA".
*   **`output/relatorio_consolidado.csv`**: O arquivo CSV com as notas consolidadas, de onde as notas (AV1, AV2, Média Final) serão extraídas.

## Saídas (Arquivos Gerados)

*   **`turma_ds.txt`**: Um novo arquivo de texto gerado na raiz do projeto. Este arquivo contém a lista de alunos na ordem exata do arquivo `ds_seduc_site.txt`, com os RAs corretos e as notas correspondentes extraídas do CSV.
    *   **Observação**: Se um aluno da lista do site não for encontrado no CSV, ele será adicionado ao arquivo com notas `0.0`, e um aviso será exibido no console.

## Uso Prático

Após gerar o `turma_ds.txt`, você pode renomeá-lo para `turma_ds_base.txt` e movê-lo para a pasta `output` para usá-lo como a lista mestra definitiva no script `mapear_notas.py`.