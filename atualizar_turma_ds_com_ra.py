import pandas as pd
import os
import re
import unicodedata

# --- Dados fornecidos pelo usuário (lista do site) ---
site_list_raw = """
ESTUDANTE	NM1	NM2	NM3	1MT	1TF
ANTORIA DE LIMA ARAÚJO
Código RA: 71768434567

...
"""

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
    """
    Lê a lista de alunos fornecida pelo site e extrai nomes e RAs.
    """
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
            i += 2 # Name and RA line
        else:
            i += 1
    return students

def gerar_turma_ds_com_ra():
    output_turma_ds_path = 'turma_ds.txt'
    grades_csv_path = os.path.join('output', 'relatorio_consolidado.csv')
    curso_alvo = 'Técnico em Desenvolvimento de Sistemas'

    # 1. Parsear a lista do site para obter nomes e RAs corretos
    print("Processando a lista de alunos fornecida pelo site...")
    site_students = parse_site_list(site_list_raw)
    if not site_students:
        print("ERRO: Nenhuma informação de aluno válida encontrada na lista do site.")
        return

    # 2. Ler o arquivo de notas
    try:
        print(f"Lendo as notas de '{grades_csv_path}'...")
        df_grades = pd.read_csv(grades_csv_path)
        df_grades.columns = ['curso', 'disciplina', 'aluno', 'av1', 'av2', 'media_final']
    except FileNotFoundError:
        print(f"ERRO: Arquivo de notas '{grades_csv_path}' não encontrado.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
        return

    # 3. Filtrar o CSV pelo curso e preparar para a junção
    df_curso = df_grades[df_grades['curso'] == curso_alvo].copy()
    if df_curso.empty:
        print(f"Nenhum dado encontrado para o curso '{curso_alvo}' no arquivo de notas.")
        return
        
    # Limpa, normaliza espaços, remove acentos e padroniza a coluna de nomes do CSV para uma comparação robusta
    df_curso['aluno_norm'] = df_curso['aluno'].str.strip().apply(normalize_whitespace).apply(strip_accents).str.upper()
    
    output_content = []
    alunos_nao_encontrados_no_csv = []

    # 4. Iterar sobre a lista do site para manter a ordem e adicionar notas
    for student_info in site_students:
        # Limpa, normaliza espaços, remove acentos e padroniza o nome do aluno da lista do site
        master_name_norm = strip_accents(normalize_whitespace(student_info['nome'].strip())).upper()
        
        match = df_curso[df_curso['aluno_norm'] == master_name_norm]
        
        if not match.empty:
            row = match.iloc[0]
            
            nm1 = f"{float(row['av1']):.1f}"
            nm2 = f"{float(row['av2']):.1f}"
            nm3 = f"{float(row['media_final']):.1f}"
            
            block = [
                student_info['nome'], # Nome original da lista do site
                student_info['ra'],   # RA original da lista do site
                "",
                nm1,
                nm2,
                nm3
            ]
            output_content.append('\n'.join(block))
        else:
            alunos_nao_encontrados_no_csv.append(student_info['nome'])
            # Adiciona um bloco com notas zeradas se o aluno não for encontrado no CSV
            block = [
                student_info['nome'],
                student_info['ra'],
                "",
                "0.0",
                "0.0",
                "0.0"
            ]
            output_content.append('\n'.join(block))

    # 5. Escrever o novo arquivo turma_ds.txt
    if output_content:
        print(f"Escrevendo novo arquivo '{output_turma_ds_path}' com RAs e notas atualizadas.")
        with open(output_turma_ds_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(output_content))
        
        print("\nProcesso concluído!")
        print(f"Arquivo '{output_turma_ds_path}' foi criado/atualizado com sucesso.")

        if alunos_nao_encontrados_no_csv:
            print("\nAviso: Os seguintes alunos da lista do site não foram encontrados no arquivo de notas e foram adicionados com notas 0.0:")
            for nome in alunos_nao_encontrados_no_csv:
                print(f" - {nome}")
    else:
        print("Nenhum aluno processado para o arquivo turma_ds.txt.")

if __name__ == '__main__':
    gerar_turma_ds_com_ra()
