# Tutorial de Automação de Notas

Este tutorial guiará você através do processo de automatizar a inserção de notas, utilizando as ferramentas gráficas e de linha de comando disponíveis neste projeto.

---

## Objetivo

O objetivo é simplificar e automatizar a inserção de notas, permitindo que você prepare os dados a partir de um relatório consolidado e, em seguida, use um script para digitar essas notas automaticamente no sistema online.

---

## Pré-requisitos

*   **Python 3.x** instalado no seu sistema.
*   **Conexão com a internet** (para instalar bibliotecas).
*   **Arquivos de dados:**
    *   `inputs/relatorio_consolidado.csv`: Seu arquivo CSV com as notas consolidadas (Curso, Disciplina, Aluno, AV1, AV2, MediaFinal).
    *   `inputs/turma_*_base.txt`: Arquivos base com a lista de alunos e RAs para cada curso.
    *   `inputs/map_disciplinas.json`: Arquivo de configuração que mapeia cursos e disciplinas.

---

## Passo 1: Configuração do Ambiente Virtual

É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto.

1.  **Abra seu terminal** (Prompt de Comando no Windows, Terminal no macOS/Linux) no diretório `b:\Dev\Notas_pygui`.

2.  **Crie o ambiente virtual:**
    ```bash
    python -m venv .venv
    ```

3.  **Ative o ambiente virtual:**
    *   **Windows:**
        ```bash
        .\.venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source ./.venv/bin/activate
        ```
    Você verá `(.venv)` no início da linha de comando, indicando que o ambiente está ativo.

4.  **Atualize as ferramentas de empacotamento:**
    ```bash
    python -m pip install --upgrade pip setuptools wheel
    ```

5.  **Instale as bibliotecas do projeto:**
    ```bash
    pip install pandas pyautogui customtkinter
    ```
    *   `pandas`: Para manipulação de dados do CSV.
    *   `pyautogui`: Para automação de teclado e mouse.
    *   `customtkinter`: Para as interfaces gráficas.

---

## Fluxo de Trabalho Recomendado (com Interfaces Gráficas)

### Passo 2.1: Gerando Arquivos de Notas (Cursos Técnicos)

Para os cursos técnicos, o primeiro passo é usar `mapear_notas.py` para converter o `relatorio_consolidado.csv` em arquivos `.txt` individuais para cada disciplina.

1.  **Certifique-se de que os arquivos base (`turma_ds_base.txt`, `turma_pj_base.txt`) e o `output/relatorio_consolidado.csv` estão no local correto.**

2.  **Execute o script `mapear_notas.py`:**
    ```bash
    python mapear_notas.py
    ```

3.  **Escolha o curso no menu** que aparecerá no terminal.

4.  **Aguarde a geração dos arquivos:**
    O script criará na pasta `output` um arquivo `.txt` para cada disciplina do curso selecionado (ex: `ds_Administracao_de_Banco_de_Dados.txt`).

### Passo 2.2: Editando Notas (Ensino Fundamental)

Para o Ensino Fundamental, as notas são inseridas ou editadas diretamente através de um formulário gráfico.

1.  **Execute o script `form_notas_ef_gui.py`:**
    ```bash
    python form_notas_ef_gui.py
    ```
2.  Na janela que abrir, **selecione a turma e o trimestre**.
3.  Clique em **"Carregar Dados"**.
4.  **Edite as notas** diretamente na tabela.
5.  Clique em **"Salvar e Gerar Arquivo de Automação"**. Isso criará o arquivo `.txt` correspondente na pasta `output` (ex: `ef8a_t1_Computação.txt`).

---

## Passo 3: Automatizando a Inserção de Notas (Todos os Cursos)

Agora que os arquivos `.txt` estão na pasta `output`, use a interface gráfica de automação.

1.  **Execute o script `automacao_notas_gui.py`:**
    ```bash
    python automacao_notas_gui.py
    ```

2.  **Selecione o Curso, a Disciplina e o Trimestre** nos menus da aplicação. As disciplinas disponíveis são detectadas automaticamente.

3.  Clique em **"Iniciar Automação"**.

4.  **Prepare o navegador:**
    A caixa de status na parte inferior da janela dará uma contagem regressiva de 10 segundos.
    *   **No navegador:** Vá para a página de inserção de notas e clique no campo da primeira nota (NM1) do primeiro aluno.

5.  **MUITO IMPORTANTE: Dê foco ao navegador!**
    **CLIQUE EM QUALQUER LUGAR NA JANELA DO SEU NAVEGADOR** antes que a contagem regressiva termine para garantir que ele esteja ativo e receba as digitações.

6.  **A automação começará** e o status será exibido na janela do programa.

---

## Fluxo de Trabalho Alternativo (Linha de Comando)

Se preferir não usar as interfaces gráficas, você pode usar os scripts originais de linha de comando.

1.  **Gere os arquivos de notas** com `python mapear_notas.py` (conforme Passo 2.1 acima).
2.  **Execute a automação** com `python automacao_notas.py`.
3.  O script pedirá para você **escolher a disciplina e o trimestre** via menus no terminal.
4.  Siga as instruções no terminal para **posicionar o cursor** e **dar foco ao navegador** antes da contagem regressiva.

---

## Dicas e Solução de Problemas

*   **Velocidade da Digitação:** Se o script estiver muito rápido ou muito lento, você pode ajustar o `time.sleep()` dentro do `automacao_notas_gui.py` ou `automacao_notas.py`.
*   **Nomes não encontrados:** Se o `mapear_notas.py` reportar alunos não encontrados, verifique a grafia e a acentuação nos seus arquivos `_base.txt` e no `relatorio_consolidado.csv`.
*   **Diagnóstico de Cursos**: Se `mapear_notas.py` não encontrar seu curso, use `python diagnosticar_csv.py` para ver os nomes exatos dos cursos presentes no seu CSV.

---

Com este tutorial, você deve ser capaz de usar os scripts de forma eficiente para automatizar a inserção de notas!
    O script começará a digitar as notas para cada aluno, usando a tecla `Tab` para navegar entre os campos.

7.  **Conclusão ou Interrupção:**
    *   Ao final, o script informará que a inserção do trimestre foi concluída e perguntará se você deseja preencher outro trimestre ou sair.
    *   Para interromper a automação a qualquer momento, pressione `Ctrl+C` no terminal.

---

## Dicas e Solução de Problemas

*   **Velocidade da Digitação:** Se o script estiver muito rápido ou muito lento, você pode ajustar o `time.sleep()` dentro do `automacao_notas.py`.
    *   `time.sleep(0.2)`: Pausa entre as notas de um mesmo aluno.
    *   `time.sleep(2.0)`: Pausa entre um aluno e outro.
*   **Nomes não encontrados:** Se o `mapear_notas.py` ainda reportar alunos não encontrados, verifique a grafia e a acentuação nos seus arquivos `_base.txt` e no `relatorio_consolidado.csv`. O script tenta normalizar, mas diferenças muito grandes podem causar falha.
*   **RAs:** Lembre-se que os RAs nos arquivos `_base.txt` são cruciais. Certifique-se de que eles estão corretos nesses arquivos.

---

Com este tutorial, você deve ser capaz de usar os scripts de forma eficiente para automatizar a inserção de notas!
