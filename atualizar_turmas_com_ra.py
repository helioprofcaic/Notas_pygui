import pandas as pd
import os
import re
import unicodedata
import json
import sys

def strip_accents(text):
    """Remove acentos de uma string."""
    try:
        text = str(text)
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
    except (TypeError, NameError):
        pass
    return str(text)

def normalize_whitespace(text):
    """Normaliza espaços em branco múltiplos para um único espaço."""
    return " ".join(str(text).split())

def parse_site_list(raw_text):
    """Lê a lista de alunos fornecida pelo site e extrai nomes e RAs."""
    students = []
    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line_content = lines[i]
        if line_content and not line_content.startswith("Código RA:") and "ESTUDANTE" not in line_content.upper():
            student_name = line_content
            ra = "RA_NAO_ENCONTRADO"
            if i + 1 < len(lines) and lines[i+1].startswith("Código RA:"):
                ra_match = re.search(r'\d+', lines[i+1])
                ra = ra_match.group(0) if ra_match else ra
            students.append({'nome': student_name.strip(), 'ra': f"Código RA: {ra}"})
            i += 2
        else:
            i += 1
    return students

def atualizar_turma(curso_config):
    """
    Função genérica para atualizar uma turma com base na configuração fornecida.
    """
    output_path = curso_config['output_file']
    site_list_path = os.path.join('inputs', curso_config['site_list'])
    curso_alvo = curso_config['nome_completo']
    grades_csv_path = os.path.join('inputs', 'relatorio_consolidado.csv')

    print(f"\n--- Processando Turma: {curso_alvo} ---")

    # 1. Ler a lista de alunos do site a partir do arquivo de entrada específico da turma
    print(f"Lendo a lista de alunos de '{site_list_path}'...")
    try:
        with open(site_list_path, 'r', encoding='utf-8') as f:
            site_list_raw = f.read()
    except FileNotFoundError:
        print(f"ERRO: O arquivo da lista do site '{site_list_path}' não foi encontrado.")
        print("Por favor, crie este arquivo com a lista de alunos copiada do site.")
        return

    # 2. Parsear a lista do site para obter nomes e RAs corretos
    site_students = parse_site_list(site_list_raw)
    if not site_students:
        print("ERRO: Nenhuma informação de aluno válida encontrada na lista do site.")
        return

    # 3. Ler o arquivo de notas
    try:
        df_grades = pd.read_csv(grades_csv_path)
        df_grades.columns = ['curso', 'disciplina', 'aluno', 'av1', 'av2', 'media_final']
    except FileNotFoundError:
        print(f"ERRO: Arquivo de notas '{grades_csv_path}' não encontrado.")
        return

    # 4. Filtrar o CSV pelo curso e preparar para a junção
    df_curso = df_grades[df_grades['curso'] == curso_alvo].copy()
    if df_curso.empty:
        print(f"AVISO: Nenhum dado encontrado para o curso '{curso_alvo}' no arquivo de notas. As notas serão zeradas.")
    
    df_curso['aluno_norm'] = df_curso['aluno'].str.strip().apply(normalize_whitespace).apply(strip_accents).str.upper()
    
    output_content = []
    alunos_nao_encontrados_no_csv = []

    # 5. Iterar sobre a lista do site para manter a ordem e adicionar notas
    for student_info in site_students:
        master_name_norm = strip_accents(normalize_whitespace(student_info['nome'].strip())).upper()
        match = df_curso[df_curso['aluno_norm'] == master_name_norm] if not df_curso.empty else pd.DataFrame()
        
        notas = ["0.0", "0.0", "0.0"]
        if not match.empty:
            row = match.iloc[0]
            notas = [f"{float(row['av1']):.1f}", f"{float(row['av2']):.1f}", f"{float(row['media_final']):.1f}"]
        else:
            alunos_nao_encontrados_no_csv.append(student_info['nome'])

        block = [student_info['nome'], student_info['ra'], ""] + notas
        output_content.append('\n'.join(block))

    # 6. Escrever o novo arquivo de saída da turma
    if output_content:
        print(f"Escrevendo novo arquivo '{output_path}' com RAs e notas atualizadas.")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(output_content))
        
        print(f"Arquivo '{output_path}' foi criado/atualizado com sucesso.")
        if alunos_nao_encontrados_no_csv:
            print(f"Aviso: {len(alunos_nao_encontrados_no_csv)} alunos não encontrados no CSV foram adicionados com notas 0.0.")
    else:
        print(f"Nenhum aluno processado para o arquivo {output_path}.")

if __name__ == '__main__':
    try:
        with open(os.path.join('inputs', 'map_disciplinas.json'), 'r', encoding='utf-8') as f:
            cursos_data = json.load(f)['cursos']
    except (FileNotFoundError, KeyError):
        print("ERRO: 'map_disciplinas.json' não encontrado ou com estrutura inválida.")
        sys.exit()

    # Filtra apenas os cursos que têm a configuração necessária para este script
    cursos_atualizaveis = {k: v for k, v in cursos_data.items() if 'site_list' in v and 'output_file' in v}
    
    if not cursos_atualizaveis:
        print("Nenhum curso configurado para atualização em 'map_disciplinas.json'.")
        print("Adicione as chaves 'site_list' e 'output_file' nas configurações dos cursos.")
        sys.exit()

    menu_options = {str(i + 1): key for i, key in enumerate(cursos_atualizaveis.keys())}

    while True:
        print("\n--- Menu de Atualização de Turmas com RA ---")
        for num, key in menu_options.items():
            print(f"[{num}] Atualizar {cursos_atualizaveis[key]['nome_completo']}")
        
        print(f"[{len(menu_options) + 1}] Atualizar TODAS as turmas")
        print("[0] Sair")
        
        escolha = input("Digite o número da sua escolha: ")

        if escolha == '0':
            print("Saindo do programa.")
            break
        elif escolha == str(len(menu_options) + 1):
            print("\n>>> INICIANDO ATUALIZAÇÃO DE TODAS AS TURMAS <<<")
            for key in cursos_atualizaveis:
                atualizar_turma(cursos_atualizaveis[key])
            print("\n>>> ATUALIZAÇÃO DE TODAS AS TURMAS CONCLUÍDA <<<")
        elif escolha in menu_options:
            curso_key_selecionado = menu_options[escolha]
            atualizar_turma(cursos_atualizaveis[curso_key_selecionado])
        else:
            print("Escolha inválida. Tente novamente.")