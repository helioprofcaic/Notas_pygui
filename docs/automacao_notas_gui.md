# Documentação: `automacao_notas_gui.py`

## Objetivo

Este script fornece uma **interface gráfica (GUI)** para o `automacao_notas.py`. Ele simplifica o processo de seleção de curso e disciplina, tornando a automação mais acessível e menos propensa a erros de digitação de nomes de arquivos.

Esta é a **maneira recomendada** de executar a automação de digitação de notas.

## Como Usar

1.  **Execute o script** a partir do terminal:
    ```bash
    python automacao_notas_gui.py
    ```
2.  **Selecione o Curso**: Use o menu suspenso para escolher o curso desejado (ex: "Técnico em Desenvolvimento de Sistemas" ou "Ensino Fundamental 9º Ano A").
3.  **Selecione a Disciplina**: O menu de disciplinas será preenchido automaticamente com as opções disponíveis na pasta `output` para o curso selecionado. Escolha a disciplina.
4.  **Selecione o Trimestre**: Marque a caixa correspondente ao trimestre que você deseja preencher (1º, 2º ou 3º).
5.  **Inicie a Automação**: Clique no botão "Iniciar Automação".
6.  **Posicionamento**: A caixa de status na parte inferior da janela instruirá você a posicionar o cursor do mouse no primeiro campo de nota (NM1) do primeiro aluno na página web.
7.  **Início da Automação**: O programa fará uma contagem regressiva de 10 segundos. **Clique na janela do navegador** durante esse tempo para garantir que ela esteja em foco. O script começará a digitar as notas e a navegar com a tecla `Tab`.

## Entradas (Arquivos Necessários)

*   **`inputs/map_disciplinas.json`**: Arquivo JSON que mapeia os cursos e suas disciplinas. É essencial para popular os menus da interface.
*   **`output/*.txt`**: Arquivos de texto gerados pelo `mapear_notas.py` ou pelo `form_notas_ef_gui.py`. A interface usa esses arquivos para determinar quais disciplinas estão disponíveis para automação.

## Saídas

Este script não gera arquivos. Sua saída é a **ação de digitação** na interface do navegador, controlada pela biblioteca `pyautogui`.

---

Para interromper a automação, você pode fechar a janela do programa ou pressionar `Ctrl+C` no terminal.