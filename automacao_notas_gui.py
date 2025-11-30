import customtkinter as ctk
import pyautogui
import time
import re
import os
import json
from threading import Thread

# --- Lógica Reutilizada do Script Original ---

def ler_dados_de_arquivo(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return None

def parse_dados(dados):
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
            if current_aluno:
                alunos.append(current_aluno)
            current_aluno = {"nome": linha, "notas": []}
        elif is_grade:
            if 'notas' in current_aluno:
                nota_str = linha.replace(',', '.')
                nota_float = float(nota_str)
                current_aluno['notas'].append(f"{nota_float:.1f}")

    if current_aluno:
        alunos.append(current_aluno)
    
    # Valida se o aluno tem 3 (técnico) ou 9 (fundamental) notas
    alunos_validos = [aluno for aluno in alunos if len(aluno.get('notas', [])) in [3, 9]]
    return alunos_validos

def sanitize_filename(name):
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '_', name)
    return name

# --- Classe da Interface Gráfica ---

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Assistente de Automação de Notas")
        self.geometry("500x450")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)

        # --- Widgets ---
        self.label_curso = ctk.CTkLabel(self, text="Selecione o Curso:", font=ctk.CTkFont(weight="bold"))
        self.label_curso.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        # Menu de seleção de curso
        self.curso_menu = ctk.CTkOptionMenu(self, values=["Carregando..."], command=self.on_course_select)
        self.curso_menu.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.label_disciplina = ctk.CTkLabel(self, text="Selecione a Disciplina:", font=ctk.CTkFont(weight="bold"))
        self.label_disciplina.grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")

        self.disciplina_menu = ctk.CTkOptionMenu(self, values=["Nenhuma disciplina encontrada"])
        self.disciplina_menu.grid(row=3, column=0, padx=20, pady=5, sticky="ew")

        self.label_trimestre = ctk.CTkLabel(self, text="Selecione o Trimestre:", font=ctk.CTkFont(weight="bold"))
        self.label_trimestre.grid(row=4, column=0, padx=20, pady=(15, 5), sticky="w")

        self.trimestre_var = ctk.StringVar(value="1")
        self.radio_frame = ctk.CTkFrame(self)
        self.radio_frame.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        self.radio_1 = ctk.CTkRadioButton(self.radio_frame, text="1º Trimestre", variable=self.trimestre_var, value="1")
        self.radio_1.pack(side="left", padx=10, pady=10)
        self.radio_2 = ctk.CTkRadioButton(self.radio_frame, text="2º Trimestre", variable=self.trimestre_var, value="2")
        self.radio_2.pack(side="left", padx=10, pady=10)
        self.radio_3 = ctk.CTkRadioButton(self.radio_frame, text="3º Trimestre", variable=self.trimestre_var, value="3")
        self.radio_3.pack(side="left", padx=10, pady=10)

        self.start_button = ctk.CTkButton(self, text="Iniciar Automação", command=self.start_automation_thread)
        self.start_button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

        self.status_textbox = ctk.CTkTextbox(self, height=100, state="disabled")
        self.status_textbox.grid(row=7, column=0, padx=20, pady=(5, 20), sticky="nsew")

        # --- Carregar dados iniciais ---
        self.cursos_data = {}
        self.selected_course_prefix = None
        self.load_initial_data()

    def log_status(self, message):
        self.status_textbox.configure(state="normal")
        self.status_textbox.insert("end", f"{message}\n")
        self.status_textbox.configure(state="disabled")
        self.status_textbox.see("end") # Auto-scroll

    def load_initial_data(self):
        try:
            with open(os.path.join('inputs', 'map_disciplinas.json'), 'r', encoding='utf-8') as f:
                self.cursos_data = json.load(f)['cursos']
        except (FileNotFoundError, KeyError):
            self.log_status("ERRO: 'map_disciplinas.json' não encontrado ou inválido.")
            self.curso_menu.configure(values=["Erro ao carregar"], state="disabled")
            self.disciplina_menu.configure(state="disabled")
            return

        if self.cursos_data:
            nomes_cursos = [data['nome_completo'] for data in self.cursos_data.values()]
            self.curso_menu.configure(values=nomes_cursos)
            self.curso_menu.set(nomes_cursos[0])
            self.on_course_select(nomes_cursos[0]) # Carrega as disciplinas do primeiro curso
        else:
            self.log_status("Nenhum curso encontrado no 'map_disciplinas.json'.")

    def on_course_select(self, selected_course_name):
        """Chamado quando um curso é selecionado no menu."""
        self.log_status(f"Curso selecionado: {selected_course_name}")
        
        # Encontra os dados do curso selecionado
        course_info = next((data for data in self.cursos_data.values() if data['nome_completo'] == selected_course_name), None)
        if not course_info:
            return

        self.selected_course_prefix = course_info['prefixo']
        disciplinas_map = course_info['disciplinas']
        output_files = os.listdir('output')
        
        is_fundamental = self.selected_course_prefix.startswith('ef')

        opcoes_disciplinas_set = set()
        for nome_completo in disciplinas_map.values():
            found_file = False
            sanitized_name = sanitize_filename(nome_completo)

            if is_fundamental:
                # Para EF, procuramos por arquivos com trimestre, ex: ef9a_t1_Computacao.txt
                # Adicionamos a disciplina se QUALQUER arquivo de trimestre existir para ela.
                for f in output_files:
                    # Padrão: ef9b_t1_Computacao.txt, ef9b_t2_Computacao.txt, etc.
                    pattern = re.compile(f"^{self.selected_course_prefix}_t[1-3]_{sanitized_name}\\.txt$")
                    if pattern.match(f):
                        found_file = True
                        break
            else:
                nome_arquivo_esperado = f"{self.selected_course_prefix}_{sanitize_filename(nome_completo)}.txt"
                if nome_arquivo_esperado in output_files:
                    found_file = True

            if found_file:
                opcoes_disciplinas_set.add(nome_completo)
        
        opcoes_disciplinas = sorted(list(opcoes_disciplinas_set))

        if opcoes_disciplinas:
            self.disciplina_menu.configure(values=opcoes_disciplinas, state="normal")
            self.disciplina_menu.set(opcoes_disciplinas[0])
        else:
            self.log_status(f"Nenhuma disciplina encontrada para '{selected_course_name}' na pasta 'output'.")
            self.log_status("Execute 'mapear_notas.py' para este curso.")
            self.disciplina_menu.configure(values=["Nenhuma disciplina disponível"], state="disabled")

    def start_automation_thread(self):
        # Usamos uma thread para não congelar a GUI durante a automação
        thread = Thread(target=self.run_automation)
        thread.start()

    def run_automation(self):
        self.start_button.configure(state="disabled", text="Executando...")
        self.status_textbox.configure(state="normal")
        self.status_textbox.delete("1.0", "end")
        self.status_textbox.configure(state="disabled")

        disciplina_selecionada = self.disciplina_menu.get()
        trimestre_num = self.trimestre_var.get()

        if not disciplina_selecionada or "Nenhuma" in disciplina_selecionada:
            self.log_status("ERRO: Nenhuma disciplina válida selecionada.")
            self.start_button.configure(state="normal", text="Iniciar Automação")
            return

        is_fundamental = self.selected_course_prefix.startswith('ef')
        if is_fundamental:
            # Constrói o nome do arquivo para EF usando o trimestre selecionado
            nome_arquivo = f"{self.selected_course_prefix}_t{trimestre_num}_{sanitize_filename(disciplina_selecionada)}.txt"
        else:
            # Mantém o nome de arquivo antigo para os cursos técnicos
            nome_arquivo = f"{self.selected_course_prefix}_{sanitize_filename(disciplina_selecionada)}.txt"

        filepath_completo = os.path.join('output', nome_arquivo)

        dados_brutos = ler_dados_de_arquivo(filepath_completo)
        if not dados_brutos:
            self.log_status(f"ERRO: Não foi possível ler o arquivo '{nome_arquivo}'.")
            self.start_button.configure(state="normal", text="Iniciar Automação")
            return

        lista_alunos = parse_dados(dados_brutos)
        if not lista_alunos:
            self.log_status("ERRO: Nenhum aluno válido encontrado no arquivo.")
            self.start_button.configure(state="normal", text="Iniciar Automação")
            return

        self.log_status(f"==> AÇÃO: Posicione o cursor no campo da PRIMEIRA NOTA (NM1) do PRIMEIRO ALUNO para o {trimestre_num}º TRIMESTRE.")
        self.log_status("A automação começará em 10 segundos...")
        
        for i in range(10, 0, -1):
            self.log_status(f"{i}...")
            time.sleep(1)
        
        self.log_status("!!! INICIANDO DIGITAÇÃO !!!")

        try:
            is_fundamental = self.selected_course_prefix.startswith('ef')
            
            for aluno in lista_alunos:
                nome_aluno = aluno['nome']
                notas_aluno = aluno['notas']
                
                notas_para_digitar = []
                if len(notas_aluno) == 3:
                    # Agora, tanto EF (do arquivo de trimestre) quanto Técnico terão 3 notas.
                    notas_para_digitar = notas_aluno
                else:
                    self.log_status(f"ERRO: Número de notas inconsistente para {nome_aluno}. Esperado 3 notas, mas encontrado {len(notas_aluno)}.")
                    continue

                self.log_status(f"-> Preenchendo para: {nome_aluno[:25]} | Notas: {', '.join(notas_para_digitar)}")

                pyautogui.write(notas_para_digitar[0])
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.write(notas_para_digitar[1])
                pyautogui.press('tab')
                time.sleep(0.2)
                pyautogui.write(notas_para_digitar[2])
                pyautogui.press('tab')
                time.sleep(2.0)

            self.log_status("\n✅ Automação concluída com sucesso!")

        except Exception as e:
            self.log_status(f"\nERRO durante a automação: {e}")
            self.log_status("Script interrompido.")
        finally:
            self.start_button.configure(state="normal", text="Iniciar Automação")

if __name__ == "__main__":
    app = App()
    app.mainloop()