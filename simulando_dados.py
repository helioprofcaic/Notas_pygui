import os
import json
import csv
import random
import shutil

# --- DADOS DE CONFIGURAÇÃO E SIMULAÇÃO ---

# Estrutura de dados que será usada para gerar o map_disciplinas.json
CURSOS_DATA = {
    "TDS": {
        "nome_completo": "Técnico em Desenvolvimento de Sistemas",
        "prefixo": "ds",
        "master_list": "turma_ds_base.txt",
        "disciplinas": {
            "FUNDTECINFOR": "Fundamentos da Tecnologia da Informação",
            "ARC": "Arquitetura de Computadores",
            "FDBD": "Fundamentos de Banco de Dados",
            "LOGPROG": "Lógica de Programação",
            "ABD": "Administração de Banco de Dados",
        }
    },
    "PJD": {
        "nome_completo": "Técnico em Programação de Jogos Digitais",
        "prefixo": "pj",
        "master_list": "turma_pj_base.txt",
        "disciplinas": {
            "FJDIG": "Fundamentos de Jogos Digitais",
            "GDRC": "Game Design",
            "AN2D": "Animação 2D",
            "PJ01": "Programação de Jogos I",
        }
    },
    "EF9A": {
        "nome_completo": "Ensino Fundamental 9º Ano A",
        "prefixo": "ef9a",
        "master_list": "turma_ef9a_base.txt",
        "disciplinas": {"COMPUT": "Computação"}
    },
    "EF8A": {
        "nome_completo": "Ensino Fundamental 8º Ano A",
        "prefixo": "ef8a",
        "master_list": "turma_ef8a_base.txt",
        "disciplinas": {"COMPUT": "Computação"}
    }
}

# Listas para gerar nomes de alunos fictícios
PRIMEIROS_NOMES = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Felipe", "Gabriela", "Heitor", "Isabela", "João", "Larissa", "Miguel", "Natália", "Otávio", "Patrícia", "Rafael", "Sofia", "Thiago", "Valentina", "William"]
SOBRENOMES = ["Silva", "Santos", "Oliveira", "Souza", "Rodrigues", "Ferreira", "Alves", "Pereira", "Lima", "Gomes", "Costa", "Ribeiro", "Martins", "Carvalho", "Almeida"]

def criar_diretorios():
    """Cria as pastas necessárias para o projeto se não existirem."""
    print("Verificando e criando diretórios...")
    os.makedirs("inputs/ef", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    print("Diretórios 'inputs/ef' e 'output' garantidos.")

def gerar_alunos_ficticios(n):
    """Gera uma lista de 'n' alunos fictícios com nome e RA."""
    alunos = []
    nomes_usados = set()
    while len(alunos) < n:
        nome = f"{random.choice(PRIMEIROS_NOMES)} {random.choice(SOBRENOMES)} {random.choice(SOBRENOMES)}"
        if nome not in nomes_usados:
            ra = f"{random.randint(10000000000, 99999999999)}"
            alunos.append({"nome": nome.upper(), "ra": f"Código RA: {ra}"})
            nomes_usados.add(nome)
    return alunos

def gerar_map_disciplinas():
    """Gera o arquivo 'inputs/map_disciplinas.json'."""
    print("Gerando 'inputs/map_disciplinas.json'...")
    filepath = os.path.join("inputs", "map_disciplinas.json")
    data = {"cursos": CURSOS_DATA}
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Arquivo JSON de mapeamento gerado.")

def gerar_listas_mestras():
    """Gera os arquivos _base.txt para cada curso."""
    print("Gerando arquivos de lista mestra (_base.txt)...")
    alunos_por_curso = {}
    for curso_key, curso_info in CURSOS_DATA.items():
        num_alunos = random.randint(20, 25)
        alunos = gerar_alunos_ficticios(num_alunos)
        alunos_por_curso[curso_key] = alunos

        pasta = "inputs/ef" if curso_key.startswith("EF") else "inputs"
        filepath = os.path.join(pasta, curso_info["master_list"])

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("ESTUDANTE\tNM1\tNM2\tNM3\t1MT\t1TF\n\n")
            for aluno in alunos:
                f.write(f"{aluno['nome']}\n")
                f.write(f"{aluno['ra']}\n\n")
        print(f" -> Arquivo '{filepath}' criado com {num_alunos} alunos.")
    return alunos_por_curso

def gerar_relatorio_csv(alunos_por_curso):
    """Gera o arquivo 'inputs/relatorio_consolidado.csv' para os cursos técnicos."""
    print("Gerando 'inputs/relatorio_consolidado.csv'...")
    filepath = os.path.join("inputs", "relatorio_consolidado.csv")
    
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Curso", "Disciplina", "Aluno", "AV1", "AV2", "MediaFinal"])

        # Itera apenas sobre os cursos técnicos
        for curso_key in ["TDS", "PJD"]:
            curso_info = CURSOS_DATA[curso_key]
            alunos = alunos_por_curso[curso_key]
            
            for disciplina_nome in curso_info["disciplinas"].values():
                for aluno in alunos:
                    av1 = round(random.uniform(4.0, 10.0), 1)
                    av2 = round(random.uniform(4.0, 10.0), 1)
                    media = round((av1 + av2) / 2 * random.uniform(0.8, 1.1), 1)
                    media = min(media, 10.0) # Garante que a média não passe de 10
                    
                    writer.writerow([
                        curso_info["nome_completo"],
                        disciplina_nome,
                        aluno["nome"],
                        av1,
                        av2,
                        media
                    ])
    print("Relatório CSV consolidado gerado com dados para cursos técnicos.")

def gerar_arquivos_output_exemplo(alunos_por_curso):
    """Gera alguns arquivos de exemplo na pasta 'output'."""
    print("Gerando arquivos de exemplo na pasta 'output'...")

    # Exemplo para curso técnico (simula o mapear_notas.py)
    curso_tds = CURSOS_DATA["TDS"]
    disciplina_abd = curso_tds["disciplinas"]["ABD"]
    filename_tds = f"{curso_tds['prefixo']}_{disciplina_abd.replace(' ', '_')}.txt"
    filepath_tds = os.path.join("output", filename_tds)
    
    with open(filepath_tds, 'w', encoding='utf-8') as f:
        for aluno in alunos_por_curso["TDS"]:
            av1 = round(random.uniform(5.0, 10.0), 1)
            av2 = round(random.uniform(5.0, 10.0), 1)
            media = round((av1 + av2) / 2, 1)
            f.write(f"{aluno['nome']}\n")
            f.write(f"{aluno['ra']}\n\n")
            f.write(f"{av1}\n{av2}\n{media}\n\n")
    print(f" -> Arquivo de exemplo gerado: '{filepath_tds}'")

    # Exemplo para Ensino Fundamental (simula o form_notas_ef_gui.py)
    curso_ef9a = CURSOS_DATA["EF9A"]
    disciplina_comp = curso_ef9a["disciplinas"]["COMPUT"]
    filename_ef = f"{curso_ef9a['prefixo']}_t1_{disciplina_comp}.txt"
    filepath_ef = os.path.join("output", filename_ef)

    with open(filepath_ef, 'w', encoding='utf-8') as f:
        for aluno in alunos_por_curso["EF9A"]:
            n1 = round(random.uniform(6.0, 10.0), 1)
            n2 = round(random.uniform(6.0, 10.0), 1)
            n3 = round(random.uniform(6.0, 10.0), 1)
            f.write(f"{aluno['nome']}\n")
            f.write(f"{aluno['ra']}\n\n")
            f.write(f"{n1}\n{n2}\n{n3}\n\n")
    print(f" -> Arquivo de exemplo gerado: '{filepath_ef}'")


def main():
    """Função principal para orquestrar a geração de dados."""
    print("--- Script de Simulação de Dados ---")
    print("\nAVISO: Este script irá criar e/ou sobrescrever os arquivos de dados")
    print("nas pastas 'inputs' e 'output'.")
    
    confirmacao = input("Deseja continuar? (s/n): ").lower()
    
    if confirmacao != 's':
        print("Operação cancelada.")
        return

    try:
        # 1. Cria as pastas
        criar_diretorios()
        
        # 2. Gera o map_disciplinas.json
        gerar_map_disciplinas()
        
        # 3. Gera os arquivos _base.txt e retorna os alunos criados
        alunos_criados = gerar_listas_mestras()
        
        # 4. Gera o relatorio_consolidado.csv com base nos alunos dos cursos técnicos
        gerar_relatorio_csv(alunos_criados)
        
        # 5. Gera arquivos de exemplo na pasta output
        gerar_arquivos_output_exemplo(alunos_criados)
        
        print("\n🎉 Simulação de dados concluída com sucesso!")
        print("O ambiente está pronto para teste.")

    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")

if __name__ == "__main__":
    main()