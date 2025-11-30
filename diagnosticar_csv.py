import pandas as pd
import os

def diagnosticar_cursos():
    """
    Lê o arquivo CSV consolidado e imprime os nomes únicos de cursos encontrados.
    """
    input_csv_path = os.path.join('inputs', 'relatorio_consolidado.csv')

    try:
        print(f"Lendo o arquivo: '{input_csv_path}'...")
        df = pd.read_csv(input_csv_path)
        
        # A primeira coluna é o curso, conforme a estrutura dos outros scripts
        coluna_curso = df.columns[0]
        
        print(f"Coluna de cursos identificada como: '{coluna_curso}'")
        
        if not df[coluna_curso].empty:
            cursos_unicos = df[coluna_curso].unique()
            print("\n--- Cursos Encontrados no Arquivo ---")
            for curso in cursos_unicos:
                print(f"- {curso}")
            print("------------------------------------")
            print("\nCopie o nome do curso exatamente como ele aparece acima e cole na sua resposta.")
        else:
            print("A coluna de cursos está vazia.")

    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada não encontrado em '{input_csv_path}'.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

if __name__ == '__main__':
    diagnosticar_cursos()
