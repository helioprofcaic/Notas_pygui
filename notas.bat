@echo off
REM %~dp0 é uma variável especial que representa o caminho completo da pasta onde este arquivo .bat está.
REM Isso garante que o comando funcione não importa onde a pasta do projeto esteja localizada.
REM Executa o script notas_cli.py usando o interpretador Python específico do ambiente virtual do projeto.

REM Define o diretório de trabalho para a pasta do projeto.
cd /d "%~dp0"

REM Executa o script como um módulo, o que resolve problemas de importação.
"%~dp0.venv\Scripts\python.exe" -m cli.notas_cli %*
