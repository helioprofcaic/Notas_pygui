import pyautogui
import time
import re
import sys
import os

import json
def ler_dados_de_arquivo(filepath):
    """Lê o conteúdo de um arquivo de texto."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"Lendo dados do arquivo: '{filepath}'")
            return f.read()
    except FileNotFoundError:
        print(f"ERRO: O arquivo '{filepath}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"ERRO ao ler o arquivo: {e}")
        return None

def parse_dados(dados):
    """Analisa o texto bruto e extrai informações dos alunos de forma robusta."""
    alunos = []
    current_aluno = {}
    
    linhas = [linha.strip() for linha in dados.strip().split('\n') if linha.strip()]

    for linha in linhas:
        is_grade = False
        try:
            float(linha.replace(',', '.'))
            is_grade = True
        except ValueError:
            is_grade = False

        if not linha.startswith('Código RA:') and not is_grade:
            if current_aluno and 'nome' in current_aluno and 'notas' in current_aluno:
                alunos.append(current_aluno)
            
            current_aluno = {"nome": linha, "notas": []}
        
        elif linha.startswith('Código RA:'):
            if 'ra' not in current_aluno:
                ra_match = re.search(r'\d+', linha)
                current_aluno['ra'] = ra_match.group(0) if ra_match else 'RA_NAO_ENCONTRADO'

        elif is_grade:
            if 'notas' in current_aluno:
                nota_str = linha.replace(',', '.')
                nota_float = float(nota_str)
                nota_formatada = f"{nota_float:.1f}"
                current_aluno['notas'].append(nota_formatada)

    if current_aluno and 'nome' in current_aluno and 'notas' in current_aluno:
        alunos.append(current_aluno)
    
    alunos_validos = []
    for aluno in alunos:
        if len(aluno.get('notas', [])) == 3:
            alunos_validos.append(aluno)
        else:
            print(f"Aviso: Aluno '{aluno.get('nome', 'NOME_DESCONHECIDO')}' foi ignorado por ter um número de notas diferente de 3.")

    return alunos_validos

def automatizar_insercao(alunos):
    """
    Automatiza a digitação de um conjunto de 3 notas para cada aluno,
    permitindo ao usuário escolher qual trimestre preencher.
    """
    if not alunos:
        print("Nenhum aluno para processar.")
        return

    print(">>> Automação de Inserção de Notas <<<")
    print("\nPara interromper o script a qualquer momento, pressione Ctrl+C no terminal.")
    print("-" * 50)

    while True:
        escolha = input("\nDigite o número do trimestre que deseja preencher (1, 2, ou 3) ou 's' para sair: ").lower()

        if escolha == 's':
            print("Saindo do programa.")
            break
        
        if escolha not in ['1', '2', '3']:
            print("Opção inválida. Por favor, digite 1, 2, 3 ou s.")
            continue

        trimestre_num = int(escolha)

        input(
            f"\n==> AÇÃO: Posicione o cursor no campo da PRIMEIRA NOTA (NM1) do PRIMEIRO ALUNO para o {trimestre_num}º TRIMESTRE e pressione Enter para começar..."
        )

        print(f"\n!!! ATENÇÃO: CLIQUE NA JANELA DO NAVEGADOR AGORA. A DIGITAÇÃO COMEÇA EM 5 SEGUNDOS !!!")
        time.sleep(5)

        print(f"Iniciando inserção para o {trimestre_num}º Trimestre...")
        for aluno in alunos:
            nome_aluno = aluno['nome']
            notas_aluno = aluno['notas']
            print(f"  -> Preenchendo para: {nome_aluno[:30]:<30} | Notas: {', '.join(notas_aluno)}")

            try:
                pyautogui.write(notas_aluno[0])
                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.write(notas_aluno[1])
                pyautogui.press('tab')
                time.sleep(0.2)

                pyautogui.write(notas_aluno[2])
                pyautogui.press('tab')
                
                time.sleep(2.0)

            except Exception as e:
                print(f"    ERRO ao processar o aluno {nome_aluno}. Erro: {e}")
                print("    Interrompendo o script. Verifique a posição do cursor e tente novamente.")
                break

        print(f"\n✅ Concluída a inserção do {trimestre_num}º Trimestre.")

    print("\n🎉 Programa finalizado!")

def sanitize_filename(name):
    """Remove caracteres inválidos de um nome de arquivo e substitui espaços."""
    # Esta função deve ser idêntica à usada no script mapear_notas.py
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '_', name)
    return name

def select_file_from_menu():
    """Exibe um menu de disciplinas baseado nos arquivos existentes e no JSON."""
    try:
        with open(os.path.join('inputs', 'map_disciplinas.json'), 'r', encoding='utf-8') as f:
            mapa_disciplinas = json.load(f)['disciplina']
    except (FileNotFoundError, KeyError):
        print("ERRO: Arquivo 'map_disciplinas.json' não encontrado ou em formato inválido na pasta 'inputs'.")
        return None

    # Inverte o mapa para facilitar a busca: {Nome Completo: Codigo}
    disciplinas_por_nome = {v: k for k, v in mapa_disciplinas.items()}
    
    # Detecta o prefixo do curso (ds_ ou pj_) com base nos arquivos em 'output'
    output_files = os.listdir('output')
    prefixo_curso = None
    if any(f.startswith('ds_') for f in output_files):
        prefixo_curso = 'ds_'
        print("Curso 'Desenvolvimento de Sistemas' detectado.")
    elif any(f.startswith('pj_') for f in output_files):
        prefixo_curso = 'pj_'
        print("Curso 'Programação de Jogos' detectado.")
    else:
        print("Nenhum arquivo de disciplina (com prefixo 'ds_' ou 'pj_') encontrado na pasta 'output'.")
        print("Execute o script 'mapear_notas.py' primeiro.")
        return None

    # Filtra as disciplinas que têm um arquivo correspondente
    opcoes_menu = []
    for nome_completo in disciplinas_por_nome.keys():
        nome_arquivo_esperado = f"{prefixo_curso}{sanitize_filename(nome_completo)}.txt"
        if nome_arquivo_esperado in output_files:
            opcoes_menu.append(nome_completo)

    if not opcoes_menu:
        print("Nenhuma disciplina correspondente aos arquivos em 'output' foi encontrada.")
        return None

    print("\n--- Selecione a Disciplina para Automação ---")
    for i, nome in enumerate(opcoes_menu):
        print(f"[{i+1}] {nome}")
    
    escolha = int(input("Digite o número da sua escolha: ")) - 1
    return f"{prefixo_curso}{sanitize_filename(opcoes_menu[escolha])}.txt"

if __name__ == "__main__":
    filepath_input = None
    # Verifica se um nome de arquivo foi passado como argumento de linha de comando
    if len(sys.argv) > 1:
        filepath_input = sys.argv[1]
    else:
        # Se não, pede para o usuário digitar
        filepath_input = select_file_from_menu()
    if filepath_input:
        # Constrói o caminho completo para o arquivo dentro da pasta 'output'
        filepath_completo = os.path.join('output', filepath_input)
        dados_brutos = ler_dados_de_arquivo(filepath_completo)
        if dados_brutos:
            lista_alunos = parse_dados(dados_brutos)
            automatizar_insercao(lista_alunos)
    else:
        print("Nenhum arquivo especificado. Saindo.")
