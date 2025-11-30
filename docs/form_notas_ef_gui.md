# Documentação: `form_notas_ef_gui.py`

## Objetivo

Este script fornece um formulário gráfico para **visualizar, editar e salvar as notas** das turmas do Ensino Fundamental. Ele foi projetado para simplificar a gestão de notas trimestrais, que são mais simples (apenas 3 notas por trimestre) em comparação com as dos cursos técnicos.

O formulário permite carregar notas de um trimestre específico, fazer ajustes e, em seguida, salvar um arquivo `.txt` formatado, pronto para ser usado pelo script `automacao_notas_gui.py`.

## Como Usar

1.  **Execute o script** a partir do terminal:
    ```bash
    python form_notas_ef_gui.py
    ```
2.  **Selecione a Turma**: No menu superior, escolha a turma do Ensino Fundamental que deseja gerenciar (ex: "Ensino Fundamental 8º Ano A").
3.  **Selecione o Trimestre**: Use os botões de rádio para selecionar o trimestre (1º, 2º ou 3º).
4.  **Carregar Dados**: Clique no botão "Carregar Dados". O formulário tentará encontrar um arquivo de notas existente na pasta `output` para a turma e trimestre selecionados. Se não encontrar, ele carregará a lista de alunos da lista mestra (ex: `turma_ef8a_base.txt`) com notas zeradas.
5.  **Edite as Notas**: Insira ou modifique as 3 notas para cada aluno diretamente nos campos de texto.
6.  **Salvar**: Após concluir a edição, clique no botão "Salvar e Gerar Arquivo de Automação".

## Entradas (Arquivos Necessários)

*   **`inputs/map_disciplinas.json`**: Usado para identificar as turmas do Ensino Fundamental e suas configurações (prefixo, lista mestra).
*   **`inputs/ef/turma_ef*_base.txt`**: Arquivos de lista mestra para cada turma do EF. São usados como base se nenhum arquivo de notas salvo for encontrado.
*   **`output/ef*_t*_* .txt`** (Opcional): Se um arquivo de notas já foi salvo para um trimestre, ele será carregado para edição.

## Saídas (Arquivos Gerados)

*   **`output/ef<turma>_t<trimestre>_Computação.txt`**: Um arquivo de texto contendo os nomes dos alunos, RAs e as 3 notas do trimestre, formatado para ser usado pelo `automacao_notas_gui.py`.