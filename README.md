# Projeto de Automação de Notas

Este projeto contém um conjunto de scripts Python para automatizar o processo de digitação de notas em sistemas acadêmicos, utilizando interfaces gráficas para facilitar o uso e minimizar erros.

## Funcionalidades Principais

*   **Interface Gráfica para Automação:** Execute a digitação de notas de forma segura e controlada através de uma GUI amigável.
*   **Formulário de Edição de Notas:** Visualize, edite e salve as notas do Ensino Fundamental de forma simples e rápida.
*   **Processamento de Dados:** Converta relatórios de notas (em formato `.csv`) em arquivos de texto (`.txt`) formatados e prontos para a automação.
*   **Scripts de Linha de Comando:** Alternativas disponíveis para usuários que preferem o terminal.

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
