# Documentação: `gerar_lista_automacao.py`

**Atenção: Este script parece ser uma versão mais antiga ou alternativa do `mapear_notas.py` e pode estar obsoleto.**

## Objetivo

O objetivo deste script é ler o `relatorio_consolidado.csv`, filtrar os dados para um curso específico (`Técnico em Desenvolvimento de Sistemas`), e gerar um único arquivo de texto (`turma_ds.txt`) formatado para o script de automação.

Diferente do `mapear_notas.py`, este script não gera arquivos por disciplina, mas sim um único arquivo grande. Além disso, ele não utiliza uma lista mestra para ordenação, ordenando os alunos alfabeticamente.

## Como Usar

```bash
python gerar_lista_automacao.py
```

## Entradas
*   **`output/relatorio_consolidado.csv`**: Arquivo com as notas consolidadas.

## Saídas
*   **`turma_ds.txt`**: Arquivo de texto na raiz do projeto com todos os alunos do curso de DS, ordenados alfabeticamente, com um placeholder "00000000000" para o RA. O usuário precisaria editar este arquivo manualmente para inserir os RAs corretos.