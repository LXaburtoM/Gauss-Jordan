import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font as tkFont
import numpy as np
from gauss_elimination import GaussElimination
from gauss_jordan import GaussJordan
import math

class ModernAlgebraCalculator:
    """
    Interfaz gráfica moderna para la calculadora de álgebra con método de eliminación de Gauss.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Calculadora de Álgebra - Gauss & Gauss-Jordan")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)
        
        # Configurar tema moderno
        self.setup_theme()
        
        # Variables
        self.num_equations = tk.StringVar(value="3")
        self.matrix_entries = []
        self.vector_entries = []
        self.gauss_solver = GaussElimination()
        self.jordan_solver = GaussJordan()
        self.method_var = tk.StringVar(value="gauss")
        self.current_step = 0
        
        # Colores del tema
        self.colors = {
            'primary': '#2E3440',      # Azul oscuro
            'secondary': '#3B4252',    # Gris azulado
            'accent': '#5E81AC',       # Azul claro
            'success': '#A3BE8C',      # Verde
            'warning': '#EBCB8B',      # Amarillo
            'error': '#BF616A',        # Rojo
            'text': '#2E3440',         # Texto oscuro
            'text_light': '#4C566A',   # Texto gris
            'background': '#ECEFF4',   # Fondo claro
            'card': '#FFFFFF'          # Fondo de tarjetas
        }
        
        self.setup_modern_ui()
        self.create_matrix_inputs()
    
    def setup_theme(self):
        """Configura el tema moderno de la aplicación."""
        style = ttk.Style()
        
        # Configurar tema base
        style.theme_use('clam')
        
        # Estilos personalizados para botones
        style.configure('Primary.TButton',
                       background='#5E81AC',
                       foreground='white',
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Primary.TButton',
                 background=[('active', '#81A1C1'),
                           ('pressed', '#4C7AA1')])
        
        style.configure('Secondary.TButton',
                       background='#A3BE8C',
                       foreground='white',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Secondary.TButton',
                 background=[('active', '#B8CC9C'),
                           ('pressed', '#8FA876')])
        
        style.configure('Warning.TButton',
                       background='#EBCB8B',
                       foreground='#2E3440',
                       font=('Segoe UI', 10),
                       borderwidth=0,
                       focuscolor='none')
        
        # Estilos para Entry
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=2,
                       relief='flat',
                       font=('Segoe UI', 10))
        
        style.configure('Error.TEntry',
                       fieldbackground='#FADBD8',
                       bordercolor='#BF616A',
                       borderwidth=2,
                       relief='flat')
        
        style.configure('Success.TEntry',
                       fieldbackground='#D5F4E6',
                       bordercolor='#A3BE8C',
                       borderwidth=2,
                       relief='flat')
        
        # Estilos para LabelFrame
        style.configure('Card.TLabelframe',
                       background='white',
                       borderwidth=1,
                       relief='solid',
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Card.TLabelframe.Label',
                       background='white',
                       foreground='#2E3440',
                       font=('Segoe UI', 11, 'bold'))
    
    def setup_modern_ui(self):
        """Configura la interfaz de usuario moderna con layout de dos columnas."""
        # Configurar fondo principal
        self.root.configure(bg='#ECEFF4')
        
        # Frame principal con padding mejorado
        main_frame = tk.Frame(self.root, bg='#ECEFF4')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header con título y descripción
        self.create_header(main_frame)
        
        # Panel de control
        self.create_control_panel(main_frame)
        
        # Frame principal dividido en dos columnas
        content_frame = tk.Frame(main_frame, bg='#ECEFF4')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Configurar grid para dos columnas
        content_frame.columnconfigure(0, weight=1, minsize=400)  # Columna izquierda - Entrada
        content_frame.columnconfigure(1, weight=2, minsize=600)  # Columna derecha - Resultados (más ancha)
        content_frame.rowconfigure(0, weight=1)
        
        # Columna izquierda - Entrada de datos y controles
        left_column = tk.Frame(content_frame, bg='#ECEFF4')
        left_column.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Columna derecha - Resultados
        right_column = tk.Frame(content_frame, bg='#ECEFF4')
        right_column.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Crear contenido de columnas
        self.create_left_column(left_column)
        self.create_right_column(right_column)
        
        # Barra de estado
        self.create_status_bar(main_frame)
    
    def create_left_column(self, parent):
        """Crea la columna izquierda con entrada de datos y controles."""
        # Panel de entrada de datos
        self.input_frame = ttk.LabelFrame(parent,
                                        text="📊 Matriz de Coeficientes y Vector Independiente",
                                        style='Card.TLabelframe',
                                        padding=15)
        self.input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Contenedor para la matriz
        self.matrix_container = tk.Frame(self.input_frame, bg='white')
        self.matrix_container.pack(fill=tk.BOTH, expand=True)
        
        # Panel de botones de acción
        self.create_action_panel(parent)
    
    def create_right_column(self, parent):
        """Crea la columna derecha con resultados."""
        # Panel de resultados
        results_frame = ttk.LabelFrame(parent,
                                     text="📈 Resultados y Proceso Paso a Paso",
                                     style='Card.TLabelframe',
                                     padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Crear notebook para organizar resultados
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de solución
        solution_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(solution_frame, text="✅ Solución")
        
        # Frame con scroll para solución
        solution_scroll_frame = tk.Frame(solution_frame, bg='white')
        solution_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.solution_text = scrolledtext.ScrolledText(solution_scroll_frame,
                                                     height=25,
                                                     width=70,
                                                     font=('Segoe UI', 10),
                                                     bg='white',
                                                     fg='#2E3440',
                                                     wrap=tk.WORD,
                                                     borderwidth=1,
                                                     relief='solid')
        self.solution_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de proceso paso a paso
        process_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(process_frame, text="🔄 Proceso")
        
        # Frame con scroll para proceso
        process_scroll_frame = tk.Frame(process_frame, bg='white')
        process_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.process_text = scrolledtext.ScrolledText(process_scroll_frame,
                                                    height=25,
                                                    width=70,
                                                    font=('Consolas', 9),
                                                    bg='white',
                                                    fg='#2E3440',
                                                    wrap=tk.WORD,
                                                    borderwidth=1,
                                                    relief='solid')
        self.process_text.pack(fill=tk.BOTH, expand=True)
    
    def create_header(self, parent):
        """Crea el header de la aplicación."""
        header_frame = tk.Frame(parent, bg='#ECEFF4', height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Título principal
        title_font = tkFont.Font(family='Segoe UI', size=24, weight='bold')
        title_label = tk.Label(header_frame, 
                              text="🧮 Calculadora de Sistemas de Ecuaciones",
                              font=title_font,
                              bg='#ECEFF4',
                              fg='#2E3440')
        title_label.pack(pady=(10, 5))
        
        # Subtítulo
        subtitle_font = tkFont.Font(family='Segoe UI', size=12)
        subtitle_label = tk.Label(header_frame,
                                 text="Métodos de Eliminación de Gauss y Gauss-Jordan",
                                 font=subtitle_font,
                                 bg='#ECEFF4',
                                 fg='#4C566A')
        subtitle_label.pack()
    
    def create_control_panel(self, parent):
        """Crea el panel de control para configuración."""
        control_frame = ttk.LabelFrame(parent, 
                                     text="⚙️ Configuración del Sistema", 
                                     style='Card.TLabelframe',
                                     padding=20)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Frame interno para controles
        controls_inner = tk.Frame(control_frame, bg='white')
        controls_inner.pack(fill=tk.X)
        
        # Label para número de ecuaciones
        eq_label = tk.Label(controls_inner,
                           text="Número de ecuaciones:",
                           font=('Segoe UI', 11),
                           bg='white',
                           fg='#2E3440')
        eq_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Spinbox con estilo moderno
        self.eq_spinbox = ttk.Spinbox(controls_inner, 
                                     from_=2, to=6, 
                                     textvariable=self.num_equations,
                                     width=8,
                                     font=('Segoe UI', 11),
                                     command=self.update_matrix_size)
        self.eq_spinbox.pack(side=tk.LEFT, padx=(0, 15))
        
        # Botón para actualizar matriz
        update_btn = ttk.Button(controls_inner,
                               text="🔄 Actualizar Matriz",
                               command=self.update_matrix_size,
                               style='Secondary.TButton')
        update_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Botón para cargar ejemplo
        example_btn = ttk.Button(controls_inner,
                                text="📝 Cargar Ejemplo",
                                command=self.load_example,
                                style='Warning.TButton')
        example_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Separador
        separator = tk.Frame(controls_inner, width=2, bg='#ECEFF4')
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        # Selección de método
        method_label = tk.Label(controls_inner,
                               text="Método:",
                               font=('Segoe UI', 11),
                               bg='white',
                               fg='#2E3440')
        method_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Frame para radiobuttons
        method_frame = tk.Frame(controls_inner, bg='white')
        method_frame.pack(side=tk.LEFT)
        
        # Radiobutton para Gauss
        gauss_rb = ttk.Radiobutton(method_frame,
                                  text="Gauss (Triangular)",
                                  variable=self.method_var,
                                  value="gauss")
        gauss_rb.pack(side=tk.LEFT, padx=(0, 10))
        
        # Radiobutton para Gauss-Jordan
        jordan_rb = ttk.Radiobutton(method_frame,
                                   text="Gauss-Jordan (Identidad)",
                                   variable=self.method_var,
                                   value="jordan")
        jordan_rb.pack(side=tk.LEFT)
    
    def create_input_panel(self, parent):
        """Crea el panel de entrada de datos."""
        self.input_frame = ttk.LabelFrame(parent,
                                        text="📊 Matriz de Coeficientes y Vector Independiente",
                                        style='Card.TLabelframe',
                                        padding=20)
        self.input_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 15))
        
        # Contenedor para la matriz con scroll
        self.matrix_container = tk.Frame(self.input_frame, bg='white')
        self.matrix_container.pack(fill=tk.BOTH, expand=True)
    
    def create_action_panel(self, parent):
        """Crea el panel de botones de acción."""
        action_frame = tk.Frame(parent, bg='#ECEFF4', height=60)
        action_frame.pack(fill=tk.X, pady=(0, 15))
        action_frame.pack_propagate(False)
        
        # Frame para centrar botones
        center_frame = tk.Frame(action_frame, bg='#ECEFF4')
        center_frame.pack(expand=True)
        
        # Botón principal para resolver
        solve_btn = ttk.Button(center_frame,
                              text="🚀 Resolver Sistema",
                              command=self.solve_system_animated,
                              style='Primary.TButton')
        solve_btn.pack(side=tk.LEFT, padx=(0, 15), ipadx=20, ipady=10)
        
        # Botón para limpiar
        clear_btn = ttk.Button(center_frame,
                              text="🗑️ Limpiar",
                              command=self.clear_all,
                              style='Secondary.TButton')
        clear_btn.pack(side=tk.LEFT, ipadx=10, ipady=10)
    
    def create_results_panel(self, parent):
        """Crea el panel de resultados con scroll mejorado."""
        results_frame = ttk.LabelFrame(parent,
                                     text="📈 Resultados y Proceso Paso a Paso",
                                     style='Card.TLabelframe',
                                     padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Crear notebook para organizar resultados
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de proceso paso a paso
        process_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(process_frame, text="🔄 Proceso")
        
        # Frame con scroll para proceso
        process_scroll_frame = tk.Frame(process_frame, bg='white')
        process_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.process_text = scrolledtext.ScrolledText(process_scroll_frame,
                                                    height=18,
                                                    width=100,
                                                    font=('Consolas', 10),
                                                    bg='white',
                                                    fg='#2E3440',
                                                    wrap=tk.WORD,
                                                    borderwidth=1,
                                                    relief='solid')
        self.process_text.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de solución
        solution_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(solution_frame, text="✅ Solución")
        
        # Frame con scroll para solución
        solution_scroll_frame = tk.Frame(solution_frame, bg='white')
        solution_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.solution_text = scrolledtext.ScrolledText(solution_scroll_frame,
                                                     height=18,
                                                     width=100,
                                                     font=('Segoe UI', 11),
                                                     bg='white',
                                                     fg='#2E3440',
                                                     wrap=tk.WORD,
                                                     borderwidth=1,
                                                     relief='solid')
        self.solution_text.pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self, parent):
        """Crea la barra de estado."""
        self.status_frame = tk.Frame(parent, bg='#3B4252', height=30)
        self.status_frame.pack(fill=tk.X)
        self.status_frame.pack_propagate(False)
        
        self.status_var = tk.StringVar(value="✨ Listo para resolver sistemas de ecuaciones")
        self.status_label = tk.Label(self.status_frame,
                                   textvariable=self.status_var,
                                   bg='#3B4252',
                                   fg='white',
                                   font=('Segoe UI', 9))
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def create_matrix_inputs(self):
        """Crea los campos de entrada para la matriz con diseño moderno."""
        try:
            n = int(self.num_equations.get())
        except ValueError:
            messagebox.showerror("❌ Error", "Número de ecuaciones debe ser un entero válido.")
            return
        
        # Limpiar entradas anteriores
        for widget in self.matrix_container.winfo_children():
            widget.destroy()
        
        self.matrix_entries = []
        self.vector_entries = []
        
        # Frame principal para la matriz
        matrix_main = tk.Frame(self.matrix_container, bg='white')
        matrix_main.pack(expand=True)
        
        # Título de sección
        title_frame = tk.Frame(matrix_main, bg='white')
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Encabezados con mejor tipografía
        header_font = tkFont.Font(family='Segoe UI', size=12, weight='bold')
        
        coeff_label = tk.Label(title_frame,
                              text="Matriz de Coeficientes [A]",
                              font=header_font,
                              bg='white',
                              fg='#2E3440')
        coeff_label.pack(side=tk.LEFT, padx=(0, 50))
        
        vector_label = tk.Label(title_frame,
                               text="Vector [b]",
                               font=header_font,
                               bg='white',
                               fg='#2E3440')
        vector_label.pack(side=tk.RIGHT, padx=(50, 0))
        
        # Frame para variables (x1, x2, x3...)
        vars_frame = tk.Frame(matrix_main, bg='white')
        vars_frame.pack(fill=tk.X, pady=(0, 10))
        
        var_font = tkFont.Font(family='Segoe UI', size=10, weight='bold')
        for j in range(n):
            var_label = tk.Label(vars_frame,
                               text=f"x{j+1}",
                               font=var_font,
                               bg='white',
                               fg='#5E81AC',
                               width=10)
            var_label.grid(row=0, column=j, padx=5)
        
        # Símbolo igual
        tk.Label(vars_frame, text="=", font=var_font, bg='white', fg='#2E3440').grid(row=0, column=n, padx=15)
        tk.Label(vars_frame, text="b", font=var_font, bg='white', fg='#5E81AC', width=10).grid(row=0, column=n+1, padx=5)
        
        # Crear campos de entrada con mejor estilo
        for i in range(n):
            # Frame para cada fila
            row_frame = tk.Frame(matrix_main, bg='white')
            row_frame.pack(fill=tk.X, pady=5)
            
            row_entries = []
            
            # Etiqueta de ecuación
            eq_font = tkFont.Font(family='Segoe UI', size=10, weight='bold')
            eq_label = tk.Label(row_frame,
                               text=f"Ec.{i+1}:",
                               font=eq_font,
                               bg='white',
                               fg='#4C566A',
                               width=6)
            eq_label.pack(side=tk.LEFT, padx=(0, 10))
            
            # Entradas para coeficientes
            entries_frame = tk.Frame(row_frame, bg='white')
            entries_frame.pack(side=tk.LEFT)
            
            for j in range(n):
                entry = tk.Entry(entries_frame,
                               width=12,
                               justify='center',
                               font=('Segoe UI', 10),
                               bg='white',
                               fg='#2E3440',
                               relief='solid',
                               borderwidth=2,
                               bd=1)
                entry.grid(row=0, column=j, padx=3, pady=2)
                entry.bind('<KeyRelease>', lambda e, r=i, c=j: self.validate_numeric_input(e, r, c))
                entry.bind('<FocusIn>', self.on_entry_focus_in)
                entry.bind('<FocusOut>', self.on_entry_focus_out)
                row_entries.append(entry)
            
            # Símbolo igual
            equal_label = tk.Label(entries_frame,
                                  text="=",
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='white',
                                  fg='#2E3440')
            equal_label.grid(row=0, column=n, padx=15)
            
            # Entrada para vector independiente
            vector_entry = tk.Entry(entries_frame,
                                  width=12,
                                  justify='center',
                                  font=('Segoe UI', 10),
                                  bg='white',
                                  fg='#2E3440',
                                  relief='solid',
                                  borderwidth=2,
                                  bd=1)
            vector_entry.grid(row=0, column=n+1, padx=3, pady=2)
            vector_entry.bind('<KeyRelease>', lambda e, r=i: self.validate_vector_input(e, r))
            vector_entry.bind('<FocusIn>', self.on_entry_focus_in)
            vector_entry.bind('<FocusOut>', self.on_entry_focus_out)
            
            self.matrix_entries.append(row_entries)
            self.vector_entries.append(vector_entry)
        
        self.status_var.set(f"📊 Matriz {n}x{n} creada. Ingrese los coeficientes.")
    
    def on_entry_focus_in(self, event):
        """Maneja el evento cuando un Entry recibe focus."""
        event.widget.configure(borderwidth=2, relief='solid')
        event.widget.configure(bg='#F8F9FA')
    
    def on_entry_focus_out(self, event):
        """Maneja el evento cuando un Entry pierde focus."""
        event.widget.configure(borderwidth=1, relief='solid')
        event.widget.configure(bg='white')
    
    def validate_numeric_input(self, event, row, col):
        """Valida entrada numérica con feedback visual mejorado."""
        widget = event.widget
        value = widget.get()
        
        if value == "" or value == "-" or value == ".":
            widget.configure(bg='white', borderwidth=1)
            return
        
        try:
            float(value)
            widget.configure(bg='#D5F4E6', borderwidth=2)  # Verde claro
            self.status_var.set(f"✅ Valor válido en posición ({row+1}, {col+1})")
        except ValueError:
            widget.configure(bg='#FADBD8', borderwidth=2)  # Rojo claro
            self.status_var.set(f"❌ Valor inválido en posición ({row+1}, {col+1}). Ingrese solo números.")
    
    def validate_vector_input(self, event, row):
        """Valida entrada del vector con feedback visual."""
        widget = event.widget
        value = widget.get()
        
        if value == "" or value == "-" or value == ".":
            widget.configure(bg='white', borderwidth=1)
            return
        
        try:
            float(value)
            widget.configure(bg='#D5F4E6', borderwidth=2)
            self.status_var.set(f"✅ Valor válido en vector, posición {row+1}")
        except ValueError:
            widget.configure(bg='#FADBD8', borderwidth=2)
            self.status_var.set(f"❌ Valor inválido en vector, posición {row+1}. Ingrese solo números.")
    
    def update_matrix_size(self):
        """Actualiza el tamaño de la matriz."""
        self.create_matrix_inputs()
        self.clear_results()
    
    def get_matrix_values(self):
        """Obtiene valores de matriz con validación mejorada."""
        try:
            n = int(self.num_equations.get())
            matrix = np.zeros((n, n))
            vector = np.zeros(n)
            
            for i in range(n):
                for j in range(n):
                    value = self.matrix_entries[i][j].get().strip()
                    if not value:
                        raise ValueError(f"Campo vacío en posición ({i+1}, {j+1})")
                    try:
                        matrix[i, j] = float(value)
                    except ValueError:
                        raise ValueError(f"Valor no numérico en posición ({i+1}, {j+1}): '{value}'")
                
                value = self.vector_entries[i].get().strip()
                if not value:
                    raise ValueError(f"Campo vacío en vector independiente, posición {i+1}")
                try:
                    vector[i] = float(value)
                except ValueError:
                    raise ValueError(f"Valor no numérico en vector independiente, posición {i+1}: '{value}'")
            
            return matrix, vector, True, ""
            
        except ValueError as e:
            return None, None, False, str(e)
    
    def solve_system_animated(self):
        """Resuelve el sistema con animaciones y feedback mejorado."""
        # Cambiar estado
        self.status_var.set("🔄 Resolviendo sistema...")
        self.root.update()
        
        # Validar entrada
        matrix, vector, valid, error_msg = self.get_matrix_values()
        
        if not valid:
            self.status_var.set("❌ Error en los datos de entrada")
            messagebox.showerror("❌ Error de Entrada", 
                               f"Error en los datos ingresados:\n{error_msg}\n\n"
                               f"Por favor, ingrese únicamente valores numéricos.")
            return
        
        # Resolver sistema usando el método seleccionado
        if self.method_var.get() == "jordan":
            solver = self.jordan_solver
            method_name = "Gauss-Jordan"
        else:
            solver = self.gauss_solver
            method_name = "Gauss"
        
        solution, has_unique_solution, error_msg = solver.solve(matrix, vector)
        
        if not has_unique_solution:
            self.status_var.set("❌ Sistema sin solución única")
            messagebox.showerror("❌ Error", error_msg)
            self.display_error_in_results(error_msg)
            return
        
        # Mostrar resultados
        self.display_solution(matrix, vector, solution, method_name, solver)
        self.display_process(solver, method_name)
        
        self.status_var.set("✅ Sistema resuelto correctamente")
        
        # Cambiar a la pestaña de solución
        self.notebook.select(1)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("🎉 Éxito", 
                           "Sistema resuelto correctamente.\n"
                           "Consulte las pestañas de Proceso y Solución para ver los detalles.")
    
    def display_solution(self, matrix, vector, solution, method_name, solver):
        """Muestra la solución con formato mejorado."""
        self.solution_text.delete('1.0', tk.END)
        
        # Título principal
        self.solution_text.insert(tk.END, "🎯 SOLUCIÓN DEL SISTEMA DE ECUACIONES\n", 'title')
        self.solution_text.insert(tk.END, f"🔧 Método: {method_name}\n", 'section_header')
        self.solution_text.insert(tk.END, "═" * 50 + "\n\n", 'separator')
        
        # Sistema original con formato matemático
        self.solution_text.insert(tk.END, "📊 Sistema Original:\n", 'section_header')
        n = len(matrix)
        for i in range(n):
            equation = f"   "
            for j in range(n):
                coeff = matrix[i, j]
                if j == 0:
                    if coeff >= 0:
                        equation += f"{coeff:8.2f}·x₁"
                    else:
                        equation += f"{coeff:8.2f}·x₁"
                else:
                    sign = " + " if coeff >= 0 else " - "
                    equation += f"{sign}{abs(coeff):7.2f}·x₁{j+1}₂"
            equation += f"  =  {vector[i]:8.2f}\n"
            self.solution_text.insert(tk.END, equation, 'equation')
        
        self.solution_text.insert(tk.END, "\n" + "─" * 50 + "\n", 'separator')
        
        # Solución con formato destacado
        self.solution_text.insert(tk.END, "✅ Solución Encontrada:\n", 'section_header')
        for i, val in enumerate(solution):
            solution_line = f"   x₁{i+1}₂ = {val:10.2f}\n"
            self.solution_text.insert(tk.END, solution_line, 'solution_value')
        
        self.solution_text.insert(tk.END, "\n" + "─" * 50 + "\n", 'separator')
        
        # Verificación
        self.solution_text.insert(tk.END, "🔍 Verificación:\n", 'section_header')
        verification = np.dot(matrix, solution)
        max_error = 0
        for i in range(n):
            error_val = abs(verification[i] - vector[i])
            max_error = max(max_error, error_val)
            status = "✅" if error_val < 1e-10 else "⚠️"
            verify_line = f"   Ecuación {i+1}: {verification[i]:10.2f} ≈ {vector[i]:10.2f}  "
            verify_line += f"(Error: {error_val:.2e}) {status}\n"
            self.solution_text.insert(tk.END, verify_line, 'verification')
        
        # Precisión general
        if max_error < 1e-10:
            precision_msg = "🎯 Excelente precisión numérica\n"
            tag = 'success'
        elif max_error < 1e-6:
            precision_msg = "👍 Buena precisión numérica\n"
            tag = 'good'
        else:
            precision_msg = "⚠️ Precisión numérica limitada\n"
            tag = 'warning'
        
        self.solution_text.insert(tk.END, f"\n{precision_msg}", tag)
        
        # Configurar tags de formato
        self.configure_solution_tags()
    
    def display_process(self, solver, method_name):
        """Muestra el proceso paso a paso con formato mejorado."""
        self.process_text.delete('1.0', tk.END)
        
        # Título
        title = "ELIMINACIÓN DE GAUSS-JORDAN" if method_name == "Gauss-Jordan" else "ELIMINACIÓN DE GAUSS"
        self.process_text.insert(tk.END, f"🔄 PROCESO DE {title}\n", 'title')
        self.process_text.insert(tk.END, "═" * 60 + "\n\n", 'separator')
        
        # Información adicional para Gauss-Jordan
        if method_name == "Gauss-Jordan":
            info_text = "🎯 Objetivo: Reducir la matriz a forma escalonada reducida (matriz identidad)\n\n"
            self.process_text.insert(tk.END, info_text, 'operation')
        
        steps = solver.get_steps()
        for i, (step_matrix, operation) in enumerate(steps):
            # Encabezado del paso
            self.process_text.insert(tk.END, f"📋 Paso {i+1}: ", 'step_header')
            self.process_text.insert(tk.END, f"{operation}\n", 'operation')
            
            # Matriz formateada
            matrix_text = solver.format_matrix(step_matrix)
            self.process_text.insert(tk.END, matrix_text + "\n", 'matrix')
            
            # Verificar si llegamos a la matriz identidad
            if method_name == "Gauss-Jordan" and hasattr(solver, 'is_identity_matrix'):
                if solver.is_identity_matrix(step_matrix):
                    self.process_text.insert(tk.END, "✨ ¡MATRIZ IDENTIDAD ALCANZADA! ✨\n", 'success')
            
            self.process_text.insert(tk.END, "\n", 'matrix')
        
        # Configurar tags de formato
        self.configure_process_tags()
    
    def configure_solution_tags(self):
        """Configura los tags de formato para la solución."""
        self.solution_text.tag_config('title', font=('Segoe UI', 14, 'bold'), foreground='#2E3440')
        self.solution_text.tag_config('section_header', font=('Segoe UI', 12, 'bold'), foreground='#5E81AC')
        self.solution_text.tag_config('separator', foreground='#4C566A')
        self.solution_text.tag_config('equation', font=('Consolas', 10), foreground='#2E3440')
        self.solution_text.tag_config('solution_value', font=('Consolas', 12, 'bold'), foreground='#A3BE8C')
        self.solution_text.tag_config('verification', font=('Consolas', 9), foreground='#4C566A')
        self.solution_text.tag_config('success', font=('Segoe UI', 10, 'bold'), foreground='#A3BE8C')
        self.solution_text.tag_config('good', font=('Segoe UI', 10, 'bold'), foreground='#5E81AC')
        self.solution_text.tag_config('warning', font=('Segoe UI', 10, 'bold'), foreground='#EBCB8B')
    
    def configure_process_tags(self):
        """Configura los tags de formato para el proceso."""
        self.process_text.tag_config('title', font=('Segoe UI', 14, 'bold'), foreground='#2E3440')
        self.process_text.tag_config('separator', foreground='#4C566A')
        self.process_text.tag_config('step_header', font=('Segoe UI', 11, 'bold'), foreground='#5E81AC')
        self.process_text.tag_config('operation', font=('Segoe UI', 10), foreground='#2E3440')
        self.process_text.tag_config('matrix', font=('Consolas', 9), foreground='#2E3440')
    
    def display_error_in_results(self, error_msg):
        """Muestra error en el área de resultados."""
        self.process_text.delete('1.0', tk.END)
        self.solution_text.delete('1.0', tk.END)
        
        error_text = f"❌ ERROR: {error_msg}\n\n"
        error_text += "Posibles causas:\n"
        error_text += "• La matriz de coeficientes es singular (determinante = 0)\n"
        error_text += "• Existe dependencia lineal entre las ecuaciones\n"
        error_text += "• El sistema puede no tener solución única\n\n"
        error_text += "Sugerencias:\n"
        error_text += "• Verifique los coeficientes ingresados\n"
        error_text += "• Asegúrese de que las ecuaciones sean linealmente independientes\n"
        error_text += "• Pruebe con un ejemplo diferente"
        
        self.solution_text.insert(tk.END, error_text)
        self.process_text.insert(tk.END, error_text)
    
    def clear_results(self):
        """Limpia las áreas de resultados."""
        self.process_text.delete('1.0', tk.END)
        self.solution_text.delete('1.0', tk.END)
        self.status_var.set("✨ Resultados limpiados")
    
    def clear_all(self):
        """Limpia todo incluyendo entradas."""
        self.clear_results()
        
        # Limpiar entradas
        for row in self.matrix_entries:
            for entry in row:
                entry.delete(0, tk.END)
                entry.configure(bg='white', borderwidth=1)
        
        for entry in self.vector_entries:
            entry.delete(0, tk.END)
            entry.configure(bg='white', borderwidth=1)
        
        self.status_var.set("🗑️ Todo limpiado. Listo para nuevos datos.")
    
    def load_example(self):
        """Carga un ejemplo con animación."""
        self.num_equations.set("3")
        self.update_matrix_size()
        
        # Ejemplo más interesante
        example_matrix = [[4, -2, 1], [3, -5, 2], [1, 1, 1]]
        example_vector = [8, -1, 6]
        
        # Llenar campos con animación
        for i in range(3):
            for j in range(3):
                entry = self.matrix_entries[i][j]
                entry.delete(0, tk.END)
                entry.insert(0, str(example_matrix[i][j]))
                entry.configure(bg='#E8F4FD', borderwidth=2)
                self.root.update()
            
            entry = self.vector_entries[i]
            entry.delete(0, tk.END)
            entry.insert(0, str(example_vector[i]))
            entry.configure(bg='#E8F4FD', borderwidth=2)
            self.root.update()
        
        self.status_var.set("📝 Ejemplo cargado: Sistema 3x3 con solución única")
        
        messagebox.showinfo("📝 Ejemplo Cargado", 
                           "Se ha cargado un ejemplo de sistema 3x3.\n\n"
                           "Sistema de ejemplo:\n"
                           "4x₁ - 2x₂ + x₃ = 8\n"
                           "3x₁ - 5x₂ + 2x₃ = -1\n"
                           "x₁ + x₂ + x₃ = 6\n\n"
                           "Presione '🚀 Resolver Sistema' para ver la solución.")

def main():
    """Función principal para ejecutar la aplicación moderna."""
    root = tk.Tk()
    
    # Configurar ícono de ventana si existe
    try:
        root.iconbitmap('calculator.ico')
    except:
        pass
    
    app = ModernAlgebraCalculator(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Configurar cierre
    root.protocol("WM_DELETE_WINDOW", lambda: root.quit())
    
    root.mainloop()

if __name__ == "__main__":
    main()
