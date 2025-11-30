import customtkinter as ctk
import json
import os
import re

def parse_master_list(filepath):
    """Lê um arquivo de lista mestra de forma robusta, ignorando cabeçalhos e linhas em branco."""
    students = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip() and "ESTUDANTE" not in line.upper()]

        i = 0
        while i < len(lines):
            # Verifica se a linha atual é um nome e a próxima é um RA
            if i + 1 < len(lines) and not lines[i].startswith("Código RA:") and lines[i+1].startswith("Código RA:"):
                student_name = lines[i]
                ra_line = lines[i+1]
                students.append({'nome': student_name, 'ra': ra_line})
                i += 2 # Pula o nome e o RA para ir para o próximo aluno
            else:
                i += 1 # Se não for um par válido, avança uma linha
    except FileNotFoundError:
        return None
    return students

def parse_grade_file(filepath):
    """Lê um arquivo de notas já preenchido, extraindo nome, RA e as 3 primeiras notas."""
    if not filepath: return None
    students = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Lê todas as linhas, mantendo as linhas em branco para a lógica de análise
            lines = [line.strip() for line in f.readlines()]

        i = 0
        while i < len(lines):
            # Procura por um bloco de aluno: Nome, seguido por RA
            line_content = lines[i]
            if line_content and not line_content.startswith("Código RA:") and "ESTUDANTE" not in line_content.upper() and i + 1 < len(lines) and lines[i+1].startswith("Código RA:"):
                student_name = lines[i]
                ra_line = lines[i+1]
                
                # A partir daqui, procura as próximas 3 linhas que são notas
                grades = []
                j = i + 2
                while j < len(lines) and len(grades) < 3:
                    if lines[j].replace('.', '', 1).isdigit():
                        grades.append(lines[j])
                    j += 1
                
                # Garante que haja 3 notas, preenchendo com "0.0" se necessário
                while len(grades) < 3:
                    grades.append("0.0")

                students.append({'nome': student_name, 'ra': ra_line, 'notas': grades[:3]})
                i = j # Continua a busca a partir de onde parou
            else:
                i += 1 # Se não for um bloco de aluno, apenas avança
    except FileNotFoundError:
        return None
    return students

def sanitize_filename(name):
    """Remove caracteres inválidos de um nome de arquivo."""
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '_', name)
    return name

class GradeEntryForm(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Formulário de Notas - Ensino Fundamental")
        self.geometry("900x700")
        ctk.set_appearance_mode("dark")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.student_entries = {}
        self.cursos_data = {}

        # --- Top Frame for Controls ---
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.top_frame.grid_columnconfigure(1, weight=1)

        self.label_curso = ctk.CTkLabel(self.top_frame, text="Selecione a Turma:", font=ctk.CTkFont(weight="bold"))
        self.label_curso.grid(row=0, column=0, padx=10, pady=10)

        self.curso_menu = ctk.CTkOptionMenu(self.top_frame, values=["Carregando..."], command=self.load_students_for_class)
        self.curso_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.load_button = ctk.CTkButton(self.top_frame, text="Carregar Dados", command=self.on_load_button_click)
        self.load_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # --- Frame para Seleção de Trimestre ---
        self.trimestre_frame = ctk.CTkFrame(self)
        self.trimestre_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self.trimestre_frame, text="Selecione o Trimestre:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        self.trimestre_var = ctk.StringVar(value="1")
        self.radio_1 = ctk.CTkRadioButton(self.trimestre_frame, text="1º Trimestre", variable=self.trimestre_var, value="1", command=self.on_trimestre_change)
        self.radio_1.pack(side="left", padx=10, pady=10)
        self.radio_2 = ctk.CTkRadioButton(self.trimestre_frame, text="2º Trimestre", variable=self.trimestre_var, value="2", command=self.on_trimestre_change)
        self.radio_2.pack(side="left", padx=10, pady=10)
        self.radio_3 = ctk.CTkRadioButton(self.trimestre_frame, text="3º Trimestre", variable=self.trimestre_var, value="3", command=self.on_trimestre_change)
        self.radio_3.pack(side="left", padx=10, pady=10)

        # --- Scrollable Frame for Student List ---
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Insira as 9 notas para cada aluno (3 por trimestre)")
        self.scrollable_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # --- Bottom Frame for Save Button ---
        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.bottom_frame.grid_columnconfigure(0, weight=1)

        self.save_button = ctk.CTkButton(self.bottom_frame, text="Salvar e Gerar Arquivo de Automação", command=self.save_grades)
        self.save_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.status_label = ctk.CTkLabel(self.bottom_frame, text="", text_color="gray")
        self.status_label.grid(row=1, column=0, padx=10, pady=(0, 10))

        self.load_initial_data()

    def load_initial_data(self):
        """Carrega os dados dos cursos do arquivo JSON."""
        try:
            with open(os.path.join('inputs', 'map_disciplinas.json'), 'r', encoding='utf-8') as f:
                all_cursos = json.load(f)['cursos']
                # Filtra apenas as turmas do Ensino Fundamental
                self.cursos_data = {k: v for k, v in all_cursos.items() if k.startswith('EF')}
        except (FileNotFoundError, KeyError):
            self.status_label.configure(text="ERRO: 'map_disciplinas.json' não encontrado ou inválido.", text_color="red")
            self.curso_menu.configure(values=["Erro"], state="disabled")
            return

        if self.cursos_data:
            nomes_cursos = [data['nome_completo'] for data in self.cursos_data.values()]
            self.curso_menu.configure(values=nomes_cursos)
            self.curso_menu.set(nomes_cursos[0])
            self.load_students_for_class(nomes_cursos[0])
        else:
            self.status_label.configure(text="Nenhuma turma do Ensino Fundamental encontrada no JSON.", text_color="yellow")

    def load_students_for_class(self, selected_class_name):
        """Limpa o frame e carrega os alunos para a turma selecionada."""
        # Limpa widgets antigos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.student_entries.clear()

        course_info = next((data for data in self.cursos_data.values() if data['nome_completo'] == selected_class_name), None)
        if not course_info:
            return

        trimestre = self.trimestre_var.get()
        prefix = course_info['prefixo']
        disciplina_nome = list(course_info['disciplinas'].values())[0]
        
        # 1. Tenta carregar o arquivo de notas da pasta 'output' de forma mais flexível.
        # Procura por qualquer arquivo que comece com o prefixo da turma e o trimestre.
        file_prefix_to_find = f"{prefix}_t{trimestre}_"
        saved_grades_path = None
        
        # Garante que a pasta 'output' exista
        if not os.path.exists('output'):
            os.makedirs('output')

        try:
            output_files = os.listdir('output')
            for filename in output_files:
                if filename.lower().startswith(file_prefix_to_find.lower()) and filename.endswith('.txt'):
                    saved_grades_path = os.path.join('output', filename)
                    break 
        except FileNotFoundError:
            pass # A pasta pode não existir, o que é tratado abaixo.
        
        students = None
        # Só tenta ler o arquivo de notas se um caminho válido foi encontrado
        if saved_grades_path:
            students = parse_grade_file(saved_grades_path)
        
        # 2. Se não encontrar, carrega da lista mestra com notas zeradas
        if students is None:
            master_list_path = os.path.join('inputs', 'ef', course_info['master_list'])
            base_students = parse_master_list(master_list_path)
            if base_students:
                # Adiciona notas zeradas para compatibilidade
                students = [{'nome': s['nome'], 'ra': s['ra'], 'notas': ["0.0", "0.0", "0.0"]} for s in base_students]
        if students is None:
            self.status_label.configure(text=f"ERRO: Arquivo base '{course_info['master_list']}' não encontrado!", text_color="red")
            return

        self.display_students(students, selected_class_name)
        self.update_headers()

    def display_students(self, students, selected_class_name):
        """Preenche a UI com a lista de alunos e suas notas."""
        # Cria cabeçalhos
        header_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=2)
        ctk.CTkLabel(header_frame, text="Aluno", font=ctk.CTkFont(weight="bold"), width=400).pack(side="left", padx=5)
        for n in range(1, 4):
            ctk.CTkLabel(header_frame, text=f"Nota {n}", width=80, anchor="center").pack(side="left", padx=2)

        # Cria uma entrada para cada aluno
        for student_info in students:
            frame = ctk.CTkFrame(self.scrollable_frame)
            frame.pack(fill="x", padx=5, pady=5)

            label = ctk.CTkLabel(frame, text=student_info['nome'], width=400, anchor="w")
            label.pack(side="left", padx=5)

            self.student_entries[student_info['nome']] = []
            for i in range(3): # Apenas 3 campos de nota
                nota = student_info.get('notas', ["0.0"]*3)[i]
                entry = ctk.CTkEntry(frame, width=80, justify="center")
                entry.insert(0, nota)
                entry.pack(side="left", padx=2, pady=5)
                self.student_entries[student_info['nome']].append(entry)
        
        self.status_label.configure(text=f"{len(students)} alunos carregados para {selected_class_name}.")

    def on_load_button_click(self):
        """Ação do botão 'Carregar Dados'."""
        self.load_students_for_class(self.curso_menu.get())

    def on_trimestre_change(self):
        """Recarrega os alunos quando o trimestre é alterado."""
        self.load_students_for_class(self.curso_menu.get())
        
    def update_headers(self):
        """Atualiza o texto do frame com o trimestre selecionado."""
        trimestre = self.trimestre_var.get()
        self.scrollable_frame.configure(label_text=f"Insira as 3 notas para o {trimestre}º Trimestre")

    def save_grades(self):
        """Coleta as notas, formata e salva no arquivo de saída."""
        selected_class_name = self.curso_menu.get()
        course_key = next((key for key, data in self.cursos_data.items() if data['nome_completo'] == selected_class_name), None)
        if not course_key:
            self.status_label.configure(text="ERRO: Turma selecionada inválida.", text_color="red")
            return

        course_info = self.cursos_data[course_key]
        prefix = course_info['prefixo']
        trimestre = self.trimestre_var.get()
        # Assume que EF só tem uma disciplina, "Computação"
        disciplina_nome = list(course_info['disciplinas'].values())[0]

        output_filename = os.path.join('output', f"{prefix}_t{trimestre}_{sanitize_filename(disciplina_nome)}.txt")
        
        master_list_path = os.path.join('inputs', 'ef', course_info['master_list'])
        output_content = []
        student_list = parse_master_list(master_list_path)
        for student_info in student_list: # Re-lê para garantir ordem e RAs
            student_name = student_info['nome']
            student_ra = student_info['ra']
            entries = self.student_entries.get(student_name, [])

            notas = []
            for entry in entries:
                try:
                    # Formata a nota para ter uma casa decimal
                    nota_val = float(entry.get().replace(',', '.'))
                    notas.append(f"{nota_val:.1f}")
                except ValueError:
                    notas.append("0.0") # Valor padrão se a entrada for inválida
            
            block = [student_name, student_ra, ""] + notas
            output_content.append('\n'.join(block))

        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(output_content))
            self.status_label.configure(text=f"Arquivo '{output_filename}' salvo com sucesso!", text_color="lightgreen")
        except Exception as e:
            self.status_label.configure(text=f"ERRO ao salvar arquivo: {e}", text_color="red")

if __name__ == "__main__":
    app = GradeEntryForm()
    app.mainloop()