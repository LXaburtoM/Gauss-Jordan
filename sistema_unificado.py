#!/usr/bin/env python3
"""
Sistema Unificado - Calculadora de Álgebra
Permite cambiar entre interfaces sin cerrar la aplicación:
1. Calculadora Mejorada v2.0 (Sistemas de ecuaciones)
2. Operaciones Matriciales (Suma y multiplicación)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from gauss_elimination_mejorado import GaussEliminationMejorado
from gauss_jordan import GaussJordan

class SistemaUnificado:
    """
    Sistema principal que integra ambas calculadoras con navegación fluida.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Unificado - Calculadora de Álgebra")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables del sistema
        self.interfaz_actual = "ecuaciones"  # "ecuaciones" o "matrices"
        
        # Variables para sistemas de ecuaciones
        self.entradas_matriz_ecuaciones = []
        self.metodo_var = tk.StringVar(value="gauss_jordan")
        self.ecuaciones_var = tk.StringVar(value="3")
        self.variables_var = tk.StringVar(value="3")
        
        # Variables para operaciones matriciales
        self.entradas_matriz_a = []
        self.entradas_matriz_b = []
        self.operacion_var = tk.StringVar(value="suma")
        self.filas_a_var = tk.StringVar(value="3")
        self.columnas_a_var = tk.StringVar(value="3")
        self.filas_b_var = tk.StringVar(value="3")
        self.columnas_b_var = tk.StringVar(value="3")
        
        # Solucionadores
        self.solucionador_gauss = GaussEliminationMejorado()
        self.solucionador_jordan = GaussJordan()
        
        # Colores del tema
        self.colores = {
            'primario': '#2c3e50',
            'secundario': '#3498db',
            'exito': '#27ae60',
            'advertencia': '#f39c12',
            'error': '#e74c3c',
            'fondo': '#f0f0f0',
            'blanco': '#ffffff',
            'texto': '#2c3e50',
            'ecuaciones': '#27ae60',
            'matrices': '#3498db'
        }
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz principal con navegación."""
        
        # Título principal con navegación
        self.crear_barra_navegacion()
        
        # Frame principal para contenido
        self.frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        self.frame_principal.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Mostrar interfaz inicial
        self.mostrar_interfaz_ecuaciones()
    
    def crear_barra_navegacion(self):
        """Crea la barra de navegación superior."""
        
        nav_frame = tk.Frame(self.root, bg=self.colores['primario'], height=80)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        # Contenedor interno para centrar contenido
        nav_content = tk.Frame(nav_frame, bg=self.colores['primario'])
        nav_content.pack(expand=True, fill='both')
        
        # Título
        titulo_label = tk.Label(
            nav_content, 
            text="🚀 SISTEMA UNIFICADO - CALCULADORA DE ÁLGEBRA",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colores['primario']
        )
        titulo_label.pack(pady=(10, 5))
        
        # Botones de navegación
        botones_frame = tk.Frame(nav_content, bg=self.colores['primario'])
        botones_frame.pack()
        
        # Botón Sistemas de Ecuaciones
        self.btn_ecuaciones = tk.Button(
            botones_frame,
            text="🧮 SISTEMAS DE ECUACIONES",
            command=self.mostrar_interfaz_ecuaciones,
            font=('Arial', 11, 'bold'),
            height=2,
            width=25,
            cursor='hand2'
        )
        self.btn_ecuaciones.pack(side='left', padx=(0, 10))
        
        # Botón Operaciones Matriciales
        self.btn_matrices = tk.Button(
            botones_frame,
            text="🔢 OPERACIONES MATRICIALES", 
            command=self.mostrar_interfaz_matrices,
            font=('Arial', 11, 'bold'),
            height=2,
            width=25,
            cursor='hand2'
        )
        self.btn_matrices.pack(side='left')
        
        # Actualizar colores de botones
        self.actualizar_botones_navegacion()
    
    def actualizar_botones_navegacion(self):
        """Actualiza el aspecto de los botones según la interfaz activa."""
        
        if self.interfaz_actual == "ecuaciones":
            self.btn_ecuaciones.configure(bg=self.colores['ecuaciones'], fg='white')
            self.btn_matrices.configure(bg='#7f8c8d', fg='white')
        else:
            self.btn_ecuaciones.configure(bg='#7f8c8d', fg='white')
            self.btn_matrices.configure(bg=self.colores['matrices'], fg='white')
    
    def limpiar_frame_principal(self):
        """Limpia el contenido del frame principal."""
        for widget in self.frame_principal.winfo_children():
            widget.destroy()
    
    def mostrar_interfaz_ecuaciones(self):
        """Muestra la interfaz de sistemas de ecuaciones."""
        
        self.interfaz_actual = "ecuaciones"
        self.actualizar_botones_navegacion()
        self.limpiar_frame_principal()
        
        # Configurar grid
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=2)
        self.frame_principal.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y entrada
        panel_izquierdo = tk.Frame(self.frame_principal, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultados
        panel_derecho = tk.Frame(self.frame_principal, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_interfaz_ecuaciones(panel_izquierdo, panel_derecho)
    
    def mostrar_interfaz_matrices(self):
        """Muestra la interfaz de operaciones matriciales."""
        
        self.interfaz_actual = "matrices"
        self.actualizar_botones_navegacion()
        self.limpiar_frame_principal()
        
        # Configurar grid
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y matrices
        panel_izquierdo = tk.Frame(self.frame_principal, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultado
        panel_derecho = tk.Frame(self.frame_principal, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_interfaz_matrices(panel_izquierdo, panel_derecho)
    
    # ==================== INTERFAZ DE SISTEMAS DE ECUACIONES ====================
    
    def crear_interfaz_ecuaciones(self, panel_izq, panel_der):
        """Crea la interfaz completa para sistemas de ecuaciones."""
        
        self.crear_panel_config_ecuaciones(panel_izq)
        self.crear_panel_matriz_ecuaciones(panel_izq)
        self.crear_panel_botones_ecuaciones(panel_izq)
        self.crear_panel_resultados_ecuaciones(panel_der)
    
    def crear_panel_config_ecuaciones(self, padre):
        """Panel de configuración para sistemas de ecuaciones."""
        
        config_frame = tk.LabelFrame(
            padre, 
            text="⚙️ Configuración del Sistema", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        config_frame.pack(fill='x', pady=(0, 10))
        
        frame_interno = tk.Frame(config_frame, bg=self.colores['fondo'])
        frame_interno.pack(fill='x', padx=15, pady=15)
        
        # Dimensiones
        tk.Label(frame_interno, text="Ecuaciones (m):", bg=self.colores['fondo']).grid(row=0, column=0, sticky='w')
        tk.Spinbox(frame_interno, from_=1, to=8, textvariable=self.ecuaciones_var, width=5).grid(row=0, column=1, padx=5)
        
        tk.Label(frame_interno, text="Variables (n):", bg=self.colores['fondo']).grid(row=0, column=2, sticky='w', padx=(20,0))
        tk.Spinbox(frame_interno, from_=1, to=8, textvariable=self.variables_var, width=5).grid(row=0, column=3, padx=5)
        
        tk.Button(frame_interno, text="Actualizar", command=self.actualizar_matriz_ecuaciones,
                 bg=self.colores['secundario'], fg='white').grid(row=0, column=4, padx=(20,0))
        
        # Método
        metodo_frame = tk.Frame(frame_interno, bg=self.colores['fondo'])
        metodo_frame.grid(row=1, column=0, columnspan=5, sticky='w', pady=(15,0))
        
        tk.Label(metodo_frame, text="Método:", bg=self.colores['fondo'], font=('Arial', 10, 'bold')).pack(side='left')
        tk.Radiobutton(metodo_frame, text="🔸 Gauss", variable=self.metodo_var, value="gauss", bg=self.colores['fondo']).pack(side='left', padx=(15,0))
        tk.Radiobutton(metodo_frame, text="💎 Gauss-Jordan", variable=self.metodo_var, value="gauss_jordan", bg=self.colores['fondo']).pack(side='left', padx=(15,0))
    
    def crear_panel_matriz_ecuaciones(self, padre):
        """Panel de entrada de matriz para ecuaciones."""
        
        self.frame_matriz_eq = tk.LabelFrame(
            padre, 
            text="📊 Sistema de Ecuaciones", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo']
        )
        self.frame_matriz_eq.pack(fill='both', expand=True, pady=(0, 10))
        
        self.actualizar_matriz_ecuaciones()
    
    def actualizar_matriz_ecuaciones(self):
        """Actualiza la matriz de entrada para ecuaciones."""
        
        try:
            m = int(self.ecuaciones_var.get())
            n = int(self.variables_var.get())
        except ValueError:
            return
        
        # Limpiar frame
        for widget in self.frame_matriz_eq.winfo_children():
            widget.destroy()
        
        # Info del sistema
        info_tipo = "CUADRADO" if m == n else ("SOBREDETERMINADO" if m > n else "SUBDETERMINADO")
        tk.Label(self.frame_matriz_eq, text=f"📋 Sistema {m}×{n} - {info_tipo}", 
                font=('Arial', 11, 'bold'), fg=self.colores['secundario'], bg=self.colores['fondo']).pack(pady=10)
        
        # Contenedor de entradas
        entrada_frame = tk.Frame(self.frame_matriz_eq, bg=self.colores['fondo'])
        entrada_frame.pack(padx=15, pady=15)
        
        # Crear entradas
        self.entradas_matriz_ecuaciones = []
        for i in range(m):
            fila = []
            for j in range(n):
                entrada = tk.Entry(entrada_frame, width=8, justify='center')
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            
            tk.Label(entrada_frame, text="=", font=('Arial', 14, 'bold'), bg=self.colores['fondo']).grid(row=i, column=n, padx=(10, 5))
            
            entrada_vector = tk.Entry(entrada_frame, width=8, justify='center', bg='#e8f8f5')
            entrada_vector.grid(row=i, column=n+1, padx=2, pady=2)
            entrada_vector.insert(0, "0")
            fila.append(entrada_vector)
            
            self.entradas_matriz_ecuaciones.append(fila)
    
    def crear_panel_botones_ecuaciones(self, padre):
        """Panel de botones para ecuaciones."""
        
        botones_frame = tk.Frame(padre, bg=self.colores['fondo'])
        botones_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(botones_frame, text="🚀 RESOLVER", command=self.resolver_ecuaciones,
                 bg=self.colores['exito'], fg='white', font=('Arial', 12, 'bold'), height=2).pack(side='left', padx=(0, 10), fill='x', expand=True)
        tk.Button(botones_frame, text="🧹 Limpiar", command=self.limpiar_ecuaciones,
                 bg=self.colores['advertencia'], fg='white', height=2).pack(side='left', padx=(0, 10))
        tk.Button(botones_frame, text="📝 Ejemplo", command=self.ejemplo_ecuaciones,
                 bg='#9b59b6', fg='white', height=2).pack(side='left')
    
    def crear_panel_resultados_ecuaciones(self, padre):
        """Panel de resultados para ecuaciones."""
        
        frame_resultados = tk.LabelFrame(padre, text="📈 Resultados", font=('Arial', 12, 'bold'), bg=self.colores['fondo'])
        frame_resultados.pack(fill='both', expand=True)
        
        self.notebook_eq = ttk.Notebook(frame_resultados)
        self.notebook_eq.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Pestaña de análisis
        frame_analisis = tk.Frame(self.notebook_eq, bg='white')
        self.notebook_eq.add(frame_analisis, text="🔍 Análisis")
        self.texto_analisis_eq = scrolledtext.ScrolledText(frame_analisis, height=25, font=('Consolas', 10), bg='white')
        self.texto_analisis_eq.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña de proceso
        frame_proceso = tk.Frame(self.notebook_eq, bg='white')
        self.notebook_eq.add(frame_proceso, text="⚡ Proceso")
        self.texto_proceso_eq = scrolledtext.ScrolledText(frame_proceso, height=25, font=('Consolas', 10), bg='white')
        self.texto_proceso_eq.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña detallada
        frame_detalle = tk.Frame(self.notebook_eq, bg='white')
        self.notebook_eq.add(frame_detalle, text="📋 Detallado")
        self.texto_detalle_eq = scrolledtext.ScrolledText(frame_detalle, height=25, font=('Consolas', 10), bg='white')
        self.texto_detalle_eq.pack(fill='both', expand=True, padx=10, pady=10)
    
    # ==================== INTERFAZ DE OPERACIONES MATRICIALES ====================
    
    def crear_interfaz_matrices(self, panel_izq, panel_der):
        """Crea la interfaz completa para operaciones matriciales."""
        
        self.crear_panel_config_matrices(panel_izq)
        self.crear_panel_entradas_matrices(panel_izq)
        self.crear_panel_botones_matrices(panel_izq)
        self.crear_panel_resultado_matrices(panel_der)
    
    def crear_panel_config_matrices(self, padre):
        """Panel de configuración para operaciones matriciales."""
        
        config_frame = tk.LabelFrame(padre, text="⚙️ Configuración", font=('Arial', 12, 'bold'), bg=self.colores['fondo'])
        config_frame.pack(fill='x', pady=(0, 10))
        
        frame_interno = tk.Frame(config_frame, bg=self.colores['fondo'])
        frame_interno.pack(fill='x', padx=15, pady=15)
        
        # Operación
        tk.Label(frame_interno, text="Operación:", bg=self.colores['fondo'], font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w')
        tk.Radiobutton(frame_interno, text="➕ Suma (A + B)", variable=self.operacion_var, value="suma", bg=self.colores['fondo'], command=self.cambiar_operacion_matriz).grid(row=1, column=0, sticky='w', padx=(20,0))
        tk.Radiobutton(frame_interno, text="✖️ Multiplicación (A × B)", variable=self.operacion_var, value="multiplicacion", bg=self.colores['fondo'], command=self.cambiar_operacion_matriz).grid(row=1, column=1, sticky='w')
        
        # Dimensiones A
        tk.Label(frame_interno, text="Matriz A:", bg=self.colores['fondo'], font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=(15,5))
        dim_a_frame = tk.Frame(frame_interno, bg=self.colores['fondo'])
        dim_a_frame.grid(row=3, column=0, columnspan=2, sticky='w')
        tk.Label(dim_a_frame, text="Filas:", bg=self.colores['fondo']).pack(side='left')
        tk.Spinbox(dim_a_frame, from_=1, to=6, textvariable=self.filas_a_var, width=5).pack(side='left', padx=5)
        tk.Label(dim_a_frame, text="Cols:", bg=self.colores['fondo']).pack(side='left', padx=(15,0))
        tk.Spinbox(dim_a_frame, from_=1, to=6, textvariable=self.columnas_a_var, width=5).pack(side='left', padx=5)
        
        # Dimensiones B
        tk.Label(frame_interno, text="Matriz B:", bg=self.colores['fondo'], font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky='w', pady=(15,5))
        dim_b_frame = tk.Frame(frame_interno, bg=self.colores['fondo'])
        dim_b_frame.grid(row=5, column=0, columnspan=2, sticky='w')
        tk.Label(dim_b_frame, text="Filas:", bg=self.colores['fondo']).pack(side='left')
        self.filas_b_spin = tk.Spinbox(dim_b_frame, from_=1, to=6, textvariable=self.filas_b_var, width=5)
        self.filas_b_spin.pack(side='left', padx=5)
        tk.Label(dim_b_frame, text="Cols:", bg=self.colores['fondo']).pack(side='left', padx=(15,0))
        self.columnas_b_spin = tk.Spinbox(dim_b_frame, from_=1, to=6, textvariable=self.columnas_b_var, width=5)
        self.columnas_b_spin.pack(side='left', padx=5)
        
        tk.Button(frame_interno, text="Actualizar", command=self.actualizar_matrices_operaciones,
                 bg=self.colores['secundario'], fg='white').grid(row=6, column=0, pady=(15,0))
    
    def crear_panel_entradas_matrices(self, padre):
        """Panel de entrada de matrices."""
        
        self.frame_matrices_op = tk.LabelFrame(padre, text="📊 Matrices", font=('Arial', 12, 'bold'), bg=self.colores['fondo'])
        self.frame_matrices_op.pack(fill='both', expand=True, pady=(0, 10))
        
        self.actualizar_matrices_operaciones()
    
    def actualizar_matrices_operaciones(self):
        """Actualiza las matrices de operaciones."""
        
        try:
            filas_a, cols_a = int(self.filas_a_var.get()), int(self.columnas_a_var.get())
            filas_b, cols_b = int(self.filas_b_var.get()), int(self.columnas_b_var.get())
        except ValueError:
            return
        
        # Limpiar frame
        for widget in self.frame_matrices_op.winfo_children():
            widget.destroy()
        
        # Canvas con scroll
        canvas = tk.Canvas(self.frame_matrices_op, bg=self.colores['fondo'])
        scrollbar = ttk.Scrollbar(self.frame_matrices_op, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colores['fondo'])
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Matriz A
        tk.Label(scrollable_frame, text=f"Matriz A ({filas_a}×{cols_a})", font=('Arial', 11, 'bold'), 
                fg=self.colores['secundario'], bg=self.colores['fondo']).pack(pady=(10, 5))
        
        frame_a = tk.Frame(scrollable_frame, bg=self.colores['fondo'])
        frame_a.pack(pady=5)
        
        self.entradas_matriz_a = []
        for i in range(filas_a):
            fila = []
            for j in range(cols_a):
                entrada = tk.Entry(frame_a, width=8, justify='center')
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            self.entradas_matriz_a.append(fila)
        
        # Matriz B
        tk.Label(scrollable_frame, text=f"Matriz B ({filas_b}×{cols_b})", font=('Arial', 11, 'bold'),
                fg=self.colores['secundario'], bg=self.colores['fondo']).pack(pady=(20, 5))
        
        frame_b = tk.Frame(scrollable_frame, bg=self.colores['fondo'])
        frame_b.pack(pady=5)
        
        self.entradas_matriz_b = []
        for i in range(filas_b):
            fila = []
            for j in range(cols_b):
                entrada = tk.Entry(frame_b, width=8, justify='center')
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            self.entradas_matriz_b.append(fila)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def cambiar_operacion_matriz(self):
        """Ajusta dimensiones según operación."""
        if self.operacion_var.get() == "suma":
            self.filas_b_var.set(self.filas_a_var.get())
            self.columnas_b_var.set(self.columnas_a_var.get())
            self.filas_b_spin.configure(state='disabled')
            self.columnas_b_spin.configure(state='disabled')
        else:
            self.filas_b_spin.configure(state='normal')
            self.columnas_b_spin.configure(state='normal')
    
    def crear_panel_botones_matrices(self, padre):
        """Panel de botones para matrices."""
        
        botones_frame = tk.Frame(padre, bg=self.colores['fondo'])
        botones_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(botones_frame, text="🚀 CALCULAR", command=self.calcular_operacion_matrices,
                 bg=self.colores['exito'], fg='white', font=('Arial', 12, 'bold'), height=2).pack(side='left', padx=(0, 10), fill='x', expand=True)
        tk.Button(botones_frame, text="🧹 Limpiar", command=self.limpiar_matrices,
                 bg=self.colores['advertencia'], fg='white', height=2).pack(side='left', padx=(0, 10))
        tk.Button(botones_frame, text="📝 Ejemplo", command=self.ejemplo_matrices,
                 bg='#9b59b6', fg='white', height=2).pack(side='left')
    
    def crear_panel_resultado_matrices(self, padre):
        """Panel de resultado para matrices."""
        
        frame_resultado = tk.LabelFrame(padre, text="📈 Resultado", font=('Arial', 12, 'bold'), bg=self.colores['fondo'])
        frame_resultado.pack(fill='both', expand=True)
        
        self.texto_resultado_mat = scrolledtext.ScrolledText(frame_resultado, height=30, font=('Consolas', 10), bg='white')
        self.texto_resultado_mat.pack(fill='both', expand=True, padx=15, pady=15)
    
    # ==================== MÉTODOS DE FUNCIONALIDAD ====================
    
    def resolver_ecuaciones(self):
        """Resuelve sistema de ecuaciones."""
        try:
            matriz, vector = self.obtener_matriz_ecuaciones()
            
            if self.metodo_var.get() == "gauss_jordan":
                solucionador = self.solucionador_jordan
                solucion, es_unica, mensaje = solucionador.resolver(matriz, vector)
                metodo_nombre = "Gauss-Jordan"
            else:
                solucionador = self.solucionador_gauss
                solucion, es_unica, mensaje = solucionador.solve(matriz, vector)
                metodo_nombre = "Gauss"
            
            self.mostrar_resultados_ecuaciones(matriz, vector, solucion, es_unica, mensaje, solucionador, metodo_nombre)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def obtener_matriz_ecuaciones(self):
        """Obtiene matriz y vector del sistema de ecuaciones."""
        try:
            m = len(self.entradas_matriz_ecuaciones)
            n = len(self.entradas_matriz_ecuaciones[0]) - 1
            
            matriz = np.zeros((m, n))
            vector = np.zeros(m)
            
            for i in range(m):
                for j in range(n):
                    valor = self.entradas_matriz_ecuaciones[i][j].get().strip()
                    matriz[i, j] = float(valor if valor else '0')
                
                valor_vector = self.entradas_matriz_ecuaciones[i][n].get().strip()
                vector[i] = float(valor_vector if valor_vector else '0')
            
            return matriz, vector
            
        except ValueError:
            raise ValueError("Error al leer valores. Verifique que todos sean números válidos.")
    
    def mostrar_resultados_ecuaciones(self, matriz, vector, solucion, es_unica, mensaje, solucionador, metodo_nombre):
        """Muestra los resultados del sistema de ecuaciones."""
        # Implementar similar a calculadora_mejorada.py pero más compacto
        self.texto_analisis_eq.delete(1.0, tk.END)
        self.texto_analisis_eq.insert(tk.END, f"SISTEMA RESUELTO:\n{mensaje}\n")
        if solucion is not None:
            self.texto_analisis_eq.insert(tk.END, f"\nSOLUCIÓN:\n")
            for i, val in enumerate(solucion):
                self.texto_analisis_eq.insert(tk.END, f"x{i+1} = {val:.4f}\n")
    
    def calcular_operacion_matrices(self):
        """Calcula operación entre matrices."""
        try:
            matriz_a, matriz_b = self.obtener_matrices_operaciones()
            operacion = self.operacion_var.get()
            
            resultado_texto = ["OPERACIÓN MATRICIAL\n" + "="*30 + "\n"]
            
            if operacion == "suma":
                if matriz_a.shape != matriz_b.shape:
                    raise ValueError("Para suma, las matrices deben tener las mismas dimensiones")
                resultado = matriz_a + matriz_b
                resultado_texto.append("OPERACIÓN: A + B\n")
            else:
                if matriz_a.shape[1] != matriz_b.shape[0]:
                    raise ValueError(f"Para multiplicación, columnas de A ({matriz_a.shape[1]}) debe igual filas de B ({matriz_b.shape[0]})")
                resultado = np.dot(matriz_a, matriz_b)
                resultado_texto.append("OPERACIÓN: A × B\n")
            
            resultado_texto.append("RESULTADO:\n")
            resultado_texto.extend(self.formatear_matriz_simple(resultado))
            
            self.texto_resultado_mat.delete(1.0, tk.END)
            self.texto_resultado_mat.insert(tk.END, "\n".join(resultado_texto))
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def obtener_matrices_operaciones(self):
        """Obtiene las matrices A y B."""
        try:
            # Matriz A
            filas_a, cols_a = len(self.entradas_matriz_a), len(self.entradas_matriz_a[0])
            matriz_a = np.zeros((filas_a, cols_a))
            for i in range(filas_a):
                for j in range(cols_a):
                    valor = self.entradas_matriz_a[i][j].get().strip()
                    matriz_a[i, j] = float(valor if valor else '0')
            
            # Matriz B
            filas_b, cols_b = len(self.entradas_matriz_b), len(self.entradas_matriz_b[0])
            matriz_b = np.zeros((filas_b, cols_b))
            for i in range(filas_b):
                for j in range(cols_b):
                    valor = self.entradas_matriz_b[i][j].get().strip()
                    matriz_b[i, j] = float(valor if valor else '0')
            
            return matriz_a, matriz_b
        except ValueError:
            raise ValueError("Error al leer valores. Verifique que sean números válidos.")
    
    def formatear_matriz_simple(self, matriz):
        """Formatea matriz para mostrar."""
        filas = []
        for fila in matriz:
            elementos = [f"{val:8.2f}" for val in fila]
            filas.append("  [" + "  ".join(elementos) + "]")
        return filas
    
    def limpiar_ecuaciones(self):
        """Limpia la interfaz de ecuaciones."""
        for fila in self.entradas_matriz_ecuaciones:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        self.texto_analisis_eq.delete(1.0, tk.END)
        self.texto_proceso_eq.delete(1.0, tk.END)
        self.texto_detalle_eq.delete(1.0, tk.END)
    
    def limpiar_matrices(self):
        """Limpia la interfaz de matrices."""
        for fila in self.entradas_matriz_a:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        for fila in self.entradas_matriz_b:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        self.texto_resultado_mat.delete(1.0, tk.END)
    
    def ejemplo_ecuaciones(self):
        """Carga ejemplo para ecuaciones."""
        # Sistema 3x3 básico
        valores = [[2, 1, -1, 8], [1, -1, 2, 0], [3, 2, 1, 11]]
        self.ecuaciones_var.set("3")
        self.variables_var.set("3")
        self.actualizar_matriz_ecuaciones()
        
        for i in range(3):
            for j in range(4):
                self.entradas_matriz_ecuaciones[i][j].delete(0, tk.END)
                self.entradas_matriz_ecuaciones[i][j].insert(0, str(valores[i][j]))
        messagebox.showinfo("Ejemplo", "Ejemplo 3×3 cargado")
    
    def ejemplo_matrices(self):
        """Carga ejemplo para matrices."""
        if self.operacion_var.get() == "suma":
            # Ejemplo suma 2x2
            self.filas_a_var.set("2")
            self.columnas_a_var.set("2")
            self.actualizar_matrices_operaciones()
            valores_a = [[1, 2], [3, 4]]
            valores_b = [[5, 6], [7, 8]]
            for i in range(2):
                for j in range(2):
                    self.entradas_matriz_a[i][j].delete(0, tk.END)
                    self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))
                    self.entradas_matriz_b[i][j].delete(0, tk.END)
                    self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))
            messagebox.showinfo("Ejemplo", "Ejemplo suma 2×2 cargado")
        else:
            # Ejemplo multiplicación 2x3 × 3x2
            self.filas_a_var.set("2")
            self.columnas_a_var.set("3")
            self.filas_b_var.set("3")
            self.columnas_b_var.set("2")
            self.actualizar_matrices_operaciones()
            valores_a = [[1, 2, 3], [4, 5, 6]]
            valores_b = [[7, 8], [9, 10], [11, 12]]
            for i in range(2):
                for j in range(3):
                    self.entradas_matriz_a[i][j].delete(0, tk.END)
                    self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))
            for i in range(3):
                for j in range(2):
                    self.entradas_matriz_b[i][j].delete(0, tk.END)
                    self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))
            messagebox.showinfo("Ejemplo", "Ejemplo multiplicación 2×3 × 3×2 cargado")


def main():
    """Función principal."""
    root = tk.Tk()
    app = SistemaUnificado(root)
    root.mainloop()


if __name__ == "__main__":
    main()
