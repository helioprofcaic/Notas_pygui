# Projeto de Automação de Notas

## Sobre o Projeto

Digitar as notas de dezenas de alunos em sistemas acadêmicos online é uma tarefa repetitiva, demorada e suscetível a erros. Este projeto nasceu para resolver esse problema, oferecendo um conjunto de ferramentas em Python que automatiza completamente o processo de inserção de notas.

A solução processa um relatório de notas consolidado (`.csv`), gera arquivos de automação individuais e, em seguida, utiliza `pyautogui` para "pilotar" o navegador, preenchendo os campos de nota de forma rápida e precisa.

### ✨ Principais Funcionalidades

*   **Flexibilidade Total:** Lida com diferentes fontes de dados, separando a lógica para turmas de cursos técnicos (via CSV) e do Ensino Fundamental (via formulário de edição).
*   **Interfaces Gráficas (GUI):** Construídas com `CustomTkinter`, as interfaces guiam o usuário de forma visual e intuitiva, desde a edição de notas até a execução da automação.
*   **Ferramenta de Linha de Comando (CLI):** Uma poderosa CLI chamada `notas` centraliza todas as operações do projeto, permitindo consultar RAs, gerar arquivos e executar scripts com comandos simples no terminal.
*   **Configuração Centralizada:** Um arquivo `map_disciplinas.json` permite configurar todas as turmas e disciplinas sem a necessidade de alterar o código-fonte.
*   **Simulação de Dados:** Um script dedicado (`simulando_dados.py`) gera um ambiente de teste completo com dados fictícios, ideal para demonstrações e desenvolvimento.

---

## Como Usar

Para um guia completo e passo a passo sobre como configurar o ambiente, preparar os arquivos e executar a automação, consulte o nosso tutorial principal:

*   **[>> Tutorial de Automação de Notas <<](./docs/tutorial.md)**

---

## Configuração Rápida (Simulação de Dados)

Se você deseja testar o projeto rapidamente sem usar dados reais, criamos um script que gera todos os arquivos de exemplo necessários.

*   **[Guia de Simulação de Dados](./docs/simulando_dados.md)**

---

## Documentação Detalhada do Projeto

Abaixo está a documentação de cada script principal do projeto. Cada link leva a uma página que explica o objetivo e o funcionamento do respectivo arquivo.

*   **[`automacao_notas_gui.py`](docs/automacao_notas_gui.md)**
*   **[`form_notas_ef_gui.py`](docs/form_notas_ef_gui.md)**
*   **[`mapear_notas.py`](docs/mapear_notas.md)**
*   **[`automacao_notas.py`](docs/automacao_notas.md)**
*   **[`relatorio_pdf.py`](docs/relatorio_pdf.md)**
*   **[`diagnosticar_csv.py`](docs/diagnosticar_csv.md)**  


---

## [Ferramenta de Linha de Comando (CLI)](./docs/notas_cli.md)

Para agilizar ainda mais o fluxo de trabalho, o projeto inclui uma poderosa ferramenta de linha de comando chamada `notas`. Com ela, você pode executar a maioria das tarefas do projeto diretamente do terminal, como consultar RAs, gerar arquivos de automação e iniciar as interfaces gráficas.

*   **>> Documentação da Ferramenta CLI (`notas`) <<**

---

## Estrutura de Pastas

*   `docs/`: Contém toda a documentação detalhada do projeto.
*   `inputs/`: Local para colocar os arquivos de entrada, como `relatorio_consolidado.csv`, `map_disciplinas.json` e as listas de alunos (`turma_*_base.txt`).
*   `output/`: Onde os scripts geram os arquivos de texto formatados, prontos para serem usados pela automação.

## Configuração

As instruções completas de configuração, incluindo a criação do ambiente virtual e a instalação das dependências (`pandas`, `pyautogui`, `customtkinter`), estão detalhadas no início do **tutorial**.

---

## Autoria e Contribuições

Este projeto foi desenvolvido por **Helio Lima**.
Professor de T.I. na escola CETI João Mendes Olímpio de Melo - Teresina, PI


Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* para relatar bugs ou sugerir melhorias, ou enviar um *pull request* com suas alterações.
