# Documentação: `automacao_notas.py`

## Objetivo

Este script automatiza o processo de inserção de notas (AV1, AV2 e Média Final) em um sistema web. Ele utiliza a biblioteca `pyautogui` para simular a digitação e a navegação entre campos, reduzindo o trabalho manual e a chance de erros.

## Como Usar

1.  **Execute o script** a partir do terminal:
    ```bash
    python automacao_notas.py
    ```
2.  **Detecção de Curso**: O script detecta automaticamente o curso (Desenvolvimento de Sistemas ou Programação de Jogos) com base nos arquivos de notas já existentes na pasta `output`.
3.  **Menu de Disciplinas**: Um menu interativo é exibido, listando as disciplinas disponíveis para automação. Escolha a disciplina desejada digitando o número correspondente.
4.  **Escolha do Trimestre**: O script perguntará qual trimestre (1, 2 ou 3) você deseja preencher.
5.  **Posicionamento**: Você será instruído a posicionar o cursor do mouse no primeiro campo de nota (NM1) do primeiro aluno na página web.
6.  **Início da Automação**: Após pressionar Enter no terminal, você terá 5 segundos para clicar na janela do navegador e garantir que ela esteja em foco. O script começará a digitar as notas e a navegar com a tecla `Tab`.

## Entradas (Arquivos Necessários)

*   **`inputs/map_disciplinas.json`**: Arquivo JSON que mapeia os códigos de disciplinas aos seus nomes completos, usado para construir o menu de seleção.
*   **`output/ds_*.txt` ou `output/pj_*.txt`**: Arquivos de texto gerados pelo `mapear_notas.py`. Cada arquivo contém a lista de alunos de uma disciplina com suas respectivas notas formatadas, prontas para serem lidas pelo script.

## Saídas

Este script não gera arquivos. Sua saída é a **ação de digitação** na interface do navegador.

## Funções Principais

*   `select_file_from_menu()`: Exibe o menu de seleção de disciplinas, detectando o curso e filtrando as opções com base nos arquivos existentes na pasta `output`.
*   `ler_dados_de_arquivo(filepath)`: Lê o conteúdo do arquivo `.txt` da disciplina selecionada.
*   `parse_dados(dados)`: Analisa o conteúdo lido e o estrutura em uma lista de dicionários, onde cada dicionário representa um aluno e suas notas.
*   `automatizar_insercao(alunos)`: Controla o fluxo de automação, interagindo com o usuário para a escolha do trimestre e executando a digitação das notas com `pyautogui`.

---

Para interromper a execução a qualquer momento, pressione `Ctrl+C` no terminal.