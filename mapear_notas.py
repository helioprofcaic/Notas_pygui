import pandas as pd
import os
import re
import unicodedata
import sys


def sanitize_filename(name):
    """Remove caracteres inválidos de um nome de arquivo."""
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '_', name)
    return name

def strip_accents(text):
    """Remove acentos de uma string, garantindo que o texto seja uma string."""
    try:
        text = str(text)
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
    except (TypeError, AttributeError):
        pass
    return str(text)

def normalize_whitespace(text):
    """Normaliza espaços em branco múltiplos para um único espaço."""
    return " ".join(str(text).split())

def parse_master_list(filepath):
    """
    Lê o arquivo mestre (como turma_ds_base.txt) e extrai a lista de alunos,
    mantendo a ordem original e ignorando cabeçalhos.
    """
    students = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
            
            i = 0
            while i < len(lines):
                line_content = lines[i]
                # Verifica se a linha não está vazia, não é um RA e não é um cabeçalho
                if line_content and not line_content.startswith("Código RA:") and "ESTUDANTE" not in line_content.upper():
                    student_name = line_content
                    ra = "RA_NAO_ENCONTRADO"
                    if i + 1 < len(lines) and lines[i+1].startswith("Código RA:"):
                        ra = lines[i+1]
                    
                    students.append({'nome': student_name.strip(), 'ra': ra})
                    # Pula para o próximo bloco potencial de nome de aluno
                    # Assumimos formato: Nome, RA, (linha em branco)
                    i += 3 
                else:
                    i += 1
    except FileNotFoundError:
        print(f"ERRO: Arquivo mestre '{filepath}' não encontrado.")
        return None
    return students

def mapear_e_gerar_arquivos(master_list_filename, curso_alvo, prefix):
    """
    Mapeia notas do CSV para a lista mestre de alunos e gera arquivos de automação
    para todas as disciplinas de um curso alvo.
    """
    master_list_filepath = os.path.join('inputs', master_list_filename)
    grades_csv_path = os.path.join('inputs', 'relatorio_consolidado.csv')
    map_json_path = os.path.join('inputs', 'map_disciplinas.json')

    # 1. Ler a lista de alunos do arquivo mestre para respeitar a ordem
    print(f"Lendo a ordem dos alunos de '{master_list_filepath}'...")
    master_students = parse_master_list(master_list_filepath)
    if master_students is None:
        return

    # Ler o mapa de disciplinas
    try:
        with open(map_json_path, 'r', encoding='utf-8') as f:
            disciplina_map = {k.upper(): v for k, v in json.load(f)['disciplina'].items()}
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        print(f"AVISO: Não foi possível carregar ou encontrar 'map_disciplinas.json'. Os nomes das disciplinas serão lidos diretamente do CSV.")
        disciplina_map = {}


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

    # 3. Filtrar o CSV pelo curso alvo
    df_curso = df_grades[df_grades['curso'] == curso_alvo].copy()
    if df_curso.empty:
        print(f"Nenhum dado encontrado para o curso '{curso_alvo}' no arquivo de notas.")
        return
        
    # Limpa, normaliza espaços, remove acentos e padroniza a coluna de nomes do CSV para uma comparação robusta
    df_curso['aluno_norm'] = df_curso['aluno'].str.strip().apply(normalize_whitespace).apply(strip_accents).str.upper()

    # Função para mapear o nome da disciplina usando o JSON
    def map_discipline_name(original_name):
        # Tenta encontrar uma correspondência direta ou por código no mapa
        for code, friendly_name in disciplina_map.items():
            if strip_accents(original_name).upper() == strip_accents(friendly_name).upper():
                return friendly_name
        return original_name # Retorna o nome original se não encontrar no mapa

    # Aplica o mapeamento na coluna de disciplinas
    df_curso['disciplina_mapeada'] = df_curso['disciplina'].apply(map_discipline_name)

    # Obter todas as disciplinas únicas para o curso selecionado
    disciplinas_unicas = df_curso['disciplina_mapeada'].unique()

    if not disciplinas_unicas.any():
        print(f"Nenhuma disciplina encontrada para o curso '{curso_alvo}'.")
        return

    print(f"\nGerando arquivos de automação para o curso: {curso_alvo}")

    for disciplina in disciplinas_unicas:
        print(f"\n--- Processando disciplina: {disciplina} ---")
        df_disciplina = df_curso[df_curso['disciplina_mapeada'] == disciplina].copy()
        
        output_filename = os.path.join('output', f"{prefix}{sanitize_filename(disciplina)}.txt")
        output_content = []
        alunos_nao_encontrados = []

        # 4. Iterar sobre a lista mestre para manter a ordem e adicionar notas
        for student_info in master_students:
            master_name_norm = strip_accents(normalize_whitespace(student_info['nome'].strip())).upper()
            
            match = df_disciplina[df_disciplina['aluno_norm'] == master_name_norm]
            
            if not match.empty:
                row = match.iloc[0]
                
                nm1 = f"{float(row['av1']):.1f}"
                nm2 = f"{float(row['av2']):.1f}"
                nm3 = f"{float(row['media_final']):.1f}"
                
                block = [
                    student_info['nome'],
                    student_info['ra'],
                    "",
                    nm1,
                    nm2,
                    nm3
                ]
                output_content.append('\n'.join(block))
            else:
                alunos_nao_encontrados.append(student_info['nome'])
                block = [
                    student_info['nome'],
                    student_info['ra'],
                    "",
                    "0.0",
                    "0.0",
                    "0.0"
                ]
                output_content.append('\n'.join(block))

        # 5. Escrever o novo arquivo de automação para a disciplina atual
        if output_content:
            print(f"Escrevendo novo arquivo de automação: '{output_filename}'")
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(output_content))
            
            print(f"Arquivo '{output_filename}' criado com sucesso.")

            if alunos_nao_encontrados:
                print("\nAviso: Os seguintes alunos da lista mestre não foram encontrados no arquivo de notas e foram adicionados com notas 0.0:")
                for nome in alunos_nao_encontrados:
                    print(f" - {nome}")
        else:
            print(f"Nenhum aluno processado para a disciplina '{disciplina}'.")

    print("\n🎉 Processo de geração de arquivos de automação concluído para todas as disciplinas do curso!")

if __name__ == '__main__':
    print("--- Gerador de Arquivos de Automação por Curso ---")
    import json # Importar json aqui também para o bloco main
    print("Escolha o curso para o qual deseja gerar os arquivos:")

    try:
        with open(os.path.join('inputs', 'map_disciplinas.json'), 'r', encoding='utf-8') as f:
            cursos_data = json.load(f)['cursos']
        
        # Cria o menu a partir do JSON
        cursos_menu = {str(i+1): key for i, key in enumerate(cursos_data.keys())}
        for num, curso_key in cursos_menu.items():
            print(f"[{num}] {cursos_data[curso_key]['nome_completo']}")

    except (FileNotFoundError, KeyError):
        print("ERRO: 'map_disciplinas.json' não encontrado ou com estrutura inválida. Não é possível continuar.")
        sys.exit()
    
    escolha_curso = input("Digite o número da sua escolha: ")

    if escolha_curso in cursos_menu:
        curso_key_selecionado = cursos_menu[escolha_curso]
        curso_info = cursos_data[curso_key_selecionado]
        mapear_e_gerar_arquivos(curso_info['master_list'], curso_info['nome_completo'], f"{curso_info['prefixo']}_")
    else:
        print("Escolha inválida. Saindo.")
