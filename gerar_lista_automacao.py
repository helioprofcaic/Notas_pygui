import pandas as pd
import os

def gerar_lista_para_automacao():
    """
    Lê o arquivo CSV consolidado, filtra, ordena, e formata os dados
    para serem usados pelo script de automação de notas.
    """
    input_csv_path = os.path.join('output', 'relatorio_consolidado.csv')
    output_txt_path = 'turma_ds.txt'
    curso_alvo = 'Técnico em Desenvolvimento de Sistemas'

    try:
        print(f"Lendo o arquivo consolidado de '{input_csv_path}'...")
        df = pd.read_csv(input_csv_path)
        # Assume as colunas originais antes da renomeação no outro script
        df.columns = ['curso', 'disciplina', 'aluno', 'av1', 'av2', 'media_final']
    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada não encontrado em '{input_csv_path}'.")
        print("Por favor, certifique-se de que o arquivo consolidado existe.")
        return
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo CSV: {e}")
        return

    print(f"Filtrando alunos do curso: '{curso_alvo}'...")
    df_curso = df[df['curso'] == curso_alvo].copy()

    if df_curso.empty:
        print(f"Nenhum aluno encontrado para o curso '{curso_alvo}'. O arquivo de saída não será gerado.")
        return

    # Aplica as transformações solicitadas
    print("Aplicando transformações: nomes em maiúsculo e ordenação alfabética...")
    df_curso['aluno'] = df_curso['aluno'].str.upper()
    df_curso = df_curso.sort_values(by='aluno').reset_index(drop=True)

    print(f"Gerando o arquivo '{output_txt_path}' para automação...")
    try:
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            for index, row in df_curso.iterrows():
                # Formata as notas para sempre terem uma casa decimal
                nm1 = f"{float(row['av1']):.1f}"
                nm2 = f"{float(row['av2']):.1f}"
                nm3 = f"{float(row['media_final']):.1f}"

                f.write(f"{row['aluno']}\n")
                # Adiciona um placeholder para o Código RA
                f.write("Código RA: 00000000000\n")
                f.write("\n") # Linha em branco
                f.write(f"{nm1}\n")
                f.write(f"{nm2}\n")
                f.write(f"{nm3}\n")
                
                # Adiciona duas linhas em branco para separar os registros de alunos
                if index < len(df_curso) - 1:
                    f.write("\n\n")

        print("\nArquivo gerado com sucesso!")
        print(f"Localização: '{os.path.abspath(output_txt_path)}'")
        print("\nAVISO IMPORTANTE:")
        print("O 'Código RA' foi preenchido com '00000000000'.")
        print(f"Você precisará editar o arquivo '{output_txt_path}' e substituir os RAs provisórios pelos corretos antes de usar na automação.")

    except Exception as e:
        print(f"Ocorreu um erro ao escrever o arquivo de saída: {e}")

if __name__ == '__main__':
    gerar_lista_para_automacao()
