# Documentação: `diagnosticar_csv.py`

## Objetivo

Este é um script de utilidade simples, projetado para ajudar a depurar problemas relacionados a nomes de cursos. Sua única função é ler o arquivo `relatorio_consolidado.csv` e imprimir no console todos os nomes de cursos únicos que ele encontrar.

Isso é útil para garantir que os nomes de cursos usados em outros scripts (como `mapear_notas.py`) correspondam **exatamente** aos nomes presentes no arquivo CSV, evitando erros de filtragem de dados.

## Como Usar

1.  **Execute o script** a partir do terminal:
    ```bash
    python diagnosticar_csv.py
    ```
2.  **Analise a Saída**: O script listará os nomes dos cursos encontrados. Você pode copiar e colar esses nomes nos locais apropriados em outros scripts para garantir a correspondência exata.

## Entradas (Arquivos Necessários)
*   **`output/relatorio_consolidado.csv`**: O arquivo CSV a ser analisado.