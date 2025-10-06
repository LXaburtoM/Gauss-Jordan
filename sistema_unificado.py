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
from independencia_lineal import IndependenciaLineal

class SistemaUnificado:
    """
    Sistema principal que integra ambas calculadoras con navegación fluida.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Unificado - Calculadora de Álgebra")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
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
        
        # Variables para independencia lineal
        self.entradas_vectores = []
        self.num_vectores_var = tk.StringVar(value="3")
        self.dimension_var = tk.StringVar(value="3")
        
        # Solucionadores
        self.solucionador_gauss = GaussEliminationMejorado()
        self.solucionador_jordan = GaussJordan()
        self.analizador_independencia = IndependenciaLineal()
        
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
        """Configura la interfaz principal con pestañas."""
        
        # Título principal
        self.crear_titulo_principal()
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Configurar estilos
        style = ttk.Style()
        style.configure('TNotebook', background=self.colores['fondo'])
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 10, 'bold'))
        
        # Crear pestañas
        self.configurar_pestana_ecuaciones()
        self.configurar_pestana_matrices()
        self.configurar_pestana_independencia()
    
    def crear_titulo_principal(self):
        """Crea el título principal de la aplicación."""
        
        titulo_frame = tk.Frame(self.root, bg=self.colores['primario'], height=60)
        titulo_frame.pack(fill='x')
        titulo_frame.pack_propagate(False)
        
        # Título centrado
        titulo_label = tk.Label(
            titulo_frame,
            text="🚀 SISTEMA UNIFICADO - CALCULADORA DE ÁLGEBRA",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg=self.colores['primario']
        )
        titulo_label.pack(expand=True)
    
    def configurar_pestana_ecuaciones(self):
        """Configura la pestaña de sistemas de ecuaciones."""
        
        # Crear frame para la pestaña
        tab_ecuaciones = tk.Frame(self.notebook, bg=self.colores['fondo'])
        self.notebook.add(tab_ecuaciones, text="🧮  Sistemas de Ecuaciones")
        
        # Configurar grid
        tab_ecuaciones.columnconfigure(0, weight=1)
        tab_ecuaciones.columnconfigure(1, weight=2)
        tab_ecuaciones.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y entrada
        panel_izquierdo = tk.Frame(tab_ecuaciones, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultados
        panel_derecho = tk.Frame(tab_ecuaciones, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_interfaz_ecuaciones(panel_izquierdo, panel_derecho)
    
    def configurar_pestana_matrices(self):
        """Configura la pestaña de operaciones matriciales."""
        
        # Crear frame para la pestaña
        tab_matrices = tk.Frame(self.notebook, bg=self.colores['fondo'])
        self.notebook.add(tab_matrices, text="🔢  Operaciones Matriciales")
        
        # Configurar grid
        tab_matrices.columnconfigure(0, weight=1)
        tab_matrices.columnconfigure(1, weight=1)
        tab_matrices.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y matrices
        panel_izquierdo = tk.Frame(tab_matrices, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultado
        panel_derecho = tk.Frame(tab_matrices, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_interfaz_matrices(panel_izquierdo, panel_derecho)
    
    def configurar_pestana_independencia(self):
        """Configura la pestaña de independencia lineal."""
        
        # Crear frame para la pestaña
        tab_independencia = tk.Frame(self.notebook, bg=self.colores['fondo'])
        self.notebook.add(tab_independencia, text="🏁  Independencia Lineal")
        
        # Configurar grid
        tab_independencia.columnconfigure(0, weight=1)
        tab_independencia.columnconfigure(1, weight=2)
        tab_independencia.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y entrada de vectores
        panel_izquierdo = tk.Frame(tab_independencia, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultados
        panel_derecho = tk.Frame(tab_independencia, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_interfaz_independencia(panel_izquierdo, panel_derecho)
    
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
        """Muestra los resultados completos del sistema de ecuaciones."""
        
        # Análisis completo
        self.texto_analisis_eq.delete(1.0, tk.END)
        
        resultado = []
        resultado.append("═" * 60)
        resultado.append("ANÁLISIS COMPLETO DEL SISTEMA DE ECUACIONES")
        resultado.append("═" * 60)
        resultado.append("")
        
        # Información básica del sistema
        m, n = matriz.shape
        resultado.append("INFORMACIÓN BÁSICA:")
        resultado.append("─" * 30)
        resultado.append(f"• Número de ecuaciones: {m}")
        resultado.append(f"• Número de variables: {n}")
        resultado.append(f"• Tipo de sistema: {self.determinar_tipo_sistema_eq(m, n)}")
        resultado.append(f"• Método utilizado: {metodo_nombre}")
        resultado.append("")
        
        # Sistema original
        resultado.append("SISTEMA ORIGINAL:")
        resultado.append("─" * 30)
        for i in range(m):
            ecuacion_partes = []
            for j in range(n):
                coef = matriz[i, j]
                if j == 0:
                    if coef == 1:
                        ecuacion_partes.append(f"x{j+1}")
                    elif coef == -1:
                        ecuacion_partes.append(f"-x{j+1}")
                    else:
                        ecuacion_partes.append(f"{coef:.2f}x{j+1}")
                else:
                    if coef > 0:
                        if coef == 1:
                            ecuacion_partes.append(f"+ x{j+1}")
                        else:
                            ecuacion_partes.append(f"+ {coef:.2f}x{j+1}")
                    elif coef < 0:
                        if coef == -1:
                            ecuacion_partes.append(f"- x{j+1}")
                        else:
                            ecuacion_partes.append(f"- {abs(coef):.2f}x{j+1}")
            
            resultado.append(f"  {' '.join(ecuacion_partes)} = {vector[i]:.2f}")
        resultado.append("")
        
        # Análisis específico para Gauss-Jordan
        if metodo_nombre == "Gauss-Jordan" and hasattr(solucionador, 'obtener_informacion_detallada'):
            info_detallada = solucionador.obtener_informacion_detallada()
            resultado.append("ANÁLISIS MATEMÁTICO:")
            resultado.append("─" * 30)
            resultado.append(f"• Rango de la matriz: {info_detallada['rango_matriz']}")
            resultado.append(f"• Rango de la matriz aumentada: {info_detallada['rango_aumentada']}")
            resultado.append(f"• Columnas pivote: {info_detallada['columnas_pivote']}")
            
            if info_detallada['variables_libres']:
                resultado.append(f"• Variables libres: {info_detallada['variables_libres']}")
                resultado.append(f"  (Total: {info_detallada['num_variables_libres']} variables libres)")
                
                # Mostrar ecuaciones de variables libres si están disponibles
                if hasattr(solucionador, 'obtener_ecuaciones_variables_libres'):
                    ecuaciones = solucionador.obtener_ecuaciones_variables_libres(
                        solucionador.pasos[-1][0] if solucionador.pasos else None, n
                    )
                    if ecuaciones:
                        resultado.append("• Ecuaciones de variables libres:")
                        for ecuacion in ecuaciones:
                            resultado.append(f"  {ecuacion}")
            else:
                resultado.append("• Variables libres: Ninguna")
            
            resultado.append(f"• Sistema consistente: {'Sí' if info_detallada['es_consistente'] else 'No'}")
            resultado.append(f"• Tipo de solución: {info_detallada['tipo_sistema'].upper()}")
            resultado.append("")
        
        # Resultado final
        resultado.append("RESULTADO:")
        resultado.append("─" * 30)
        resultado.append(mensaje)
        resultado.append("")
        
        if solucion is not None:
            resultado.append("SOLUCIÓN:")
            resultado.append("─" * 30)
            if not es_unica:
                resultado.append("(Solución particular con variables libres = 0)")
            
            for i, valor in enumerate(solucion):
                resultado.append(f"  x{i+1} = {valor:.4f}")
            
            # Verificación de la solución
            resultado.append("")
            resultado.append("VERIFICACIÓN:")
            resultado.append("─" * 30)
            verificacion = np.dot(matriz, solucion)
            for i in range(len(vector)):
                error = abs(verificacion[i] - vector[i])
                estado = "✓" if error < 1e-10 else "≈"
                resultado.append(f"  Ecuación {i+1}: {verificacion[i]:.4f} = {vector[i]:.4f} {estado}")
        
        resultado.append("")
        resultado.append("═" * 60)
        
        self.texto_analisis_eq.insert(tk.END, "\n".join(resultado))
        
        # Mostrar proceso paso a paso
        self.mostrar_proceso_ecuaciones(solucionador, metodo_nombre)
        
        # Mostrar información detallada según el método
        if metodo_nombre == "Gauss-Jordan":
            self.mostrar_detalle_gauss_jordan(solucionador)
        elif metodo_nombre == "Gauss":
            self.mostrar_informacion_gauss(solucionador)
    
    def determinar_tipo_sistema_eq(self, m, n):
        """Determina el tipo de sistema según el número de ecuaciones y variables."""
        if m == n:
            return "Cuadrado"
        elif m > n:
            return "Sobredeterminado"
        else:
            return "Subdeterminado"
    
    def mostrar_proceso_ecuaciones(self, solucionador, metodo_nombre):
        """Muestra el proceso paso a paso del método utilizado."""
        
        self.texto_proceso_eq.delete(1.0, tk.END)
        
        contenido = []
        contenido.append("═" * 60)
        contenido.append(f"PROCESO PASO A PASO - MÉTODO {metodo_nombre.upper()}")
        contenido.append("═" * 60)
        contenido.append("")
        
        # Obtener pasos del proceso
        if hasattr(solucionador, 'obtener_pasos'):
            pasos = solucionador.obtener_pasos()
        elif hasattr(solucionador, 'get_steps'):
            pasos = solucionador.get_steps()
        else:
            contenido.append("No hay pasos disponibles para mostrar.")
            self.texto_proceso_eq.insert(tk.END, "\n".join(contenido))
            return
        
        for i, (matriz_paso, operacion) in enumerate(pasos):
            contenido.append(f"PASO {i+1}:")
            contenido.append("─" * 20)
            contenido.append(f"Operación: {operacion}")
            contenido.append("")
            contenido.append("Matriz resultante:")
            
            # Formatear matriz
            if hasattr(solucionador, 'formatear_matriz'):
                matriz_formateada = solucionador.formatear_matriz(matriz_paso)
                contenido.append(matriz_formateada)
            elif hasattr(solucionador, 'format_matrix'):
                matriz_formateada = solucionador.format_matrix(matriz_paso)
                contenido.append(matriz_formateada)
            else:
                # Formateo básico si no hay método específico
                for fila in matriz_paso:
                    fila_formateada = []
                    for val in fila[:-1]:
                        fila_formateada.append(f"{val:8.2f}")
                    fila_formateada.append(" |")
                    fila_formateada.append(f"{fila[-1]:8.2f}")
                    contenido.append("  " + " ".join(fila_formateada))
            
            contenido.append("")
            contenido.append("")
        
        contenido.append("═" * 60)
        contenido.append("PROCESO COMPLETADO")
        contenido.append("═" * 60)
        
        self.texto_proceso_eq.insert(tk.END, "\n".join(contenido))
    
    def mostrar_detalle_gauss_jordan(self, solucionador):
        """Muestra información específica y detallada para el método Gauss-Jordan."""
        
        self.texto_detalle_eq.delete(1.0, tk.END)
        
        if not hasattr(solucionador, 'obtener_informacion_detallada'):
            self.texto_detalle_eq.insert(tk.END, "Información detallada no disponible para este método.")
            return
        
        info = solucionador.obtener_informacion_detallada()
        
        contenido = []
        contenido.append("═" * 60)
        contenido.append("INFORMACIÓN DETALLADA - MÉTODO GAUSS-JORDAN")
        contenido.append("═" * 60)
        contenido.append("")
        
        contenido.append("ANÁLISIS ESTRUCTURAL:")
        contenido.append("─" * 30)
        contenido.append(f"• Rango de la matriz de coeficientes: {info['rango_matriz']}")
        contenido.append(f"• Rango de la matriz aumentada: {info['rango_aumentada']}")
        contenido.append(f"• Diferencia de rangos: {info['rango_aumentada'] - info['rango_matriz']}")
        contenido.append("")
        
        contenido.append("COLUMNAS PIVOTE:")
        contenido.append("─" * 30)
        if info['columnas_pivote']:
            contenido.append(f"• Posiciones: {info['columnas_pivote']}")
            contenido.append(f"• Total: {len(info['columnas_pivote'])} columnas pivote")
            contenido.append("• Estas columnas contienen las variables básicas del sistema")
        else:
            contenido.append("• No se encontraron columnas pivote")
        contenido.append("")
        
        contenido.append("VARIABLES LIBRES:")
        contenido.append("─" * 30)
        if info['variables_libres']:
            contenido.append(f"• Variables libres: {info['variables_libres']}")
            contenido.append(f"• Cantidad: {info['num_variables_libres']}")
            contenido.append("• Estas variables pueden tomar cualquier valor real")
            contenido.append("• La solución mostrada asigna valor 0 a las variables libres")
        else:
            contenido.append("• No hay variables libres")
            contenido.append("• Todas las variables están determinadas por el sistema")
        contenido.append("")
        
        contenido.append("CLASIFICACIÓN DEL SISTEMA:")
        contenido.append("─" * 30)
        contenido.append(f"• Consistencia: {'Consistente' if info['es_consistente'] else 'Inconsistente'}")
        contenido.append(f"• Tipo de solución: {info['tipo_sistema'].upper()}")
        
        if info['tipo_sistema'] == 'unico':
            contenido.append("  → El sistema tiene una única solución")
        elif info['tipo_sistema'] == 'infinito':
            contenido.append("  → El sistema tiene infinitas soluciones")
            contenido.append(f"  → Dimensión del espacio de soluciones: {info['num_variables_libres']}")
        else:
            contenido.append("  → El sistema no tiene solución")
        
        contenido.append("")
        
        contenido.append("INTERPRETACIÓN GEOMÉTRICA:")
        contenido.append("─" * 30)
        if info['tipo_sistema'] == 'unico':
            contenido.append("• Las ecuaciones se intersectan en un único punto")
        elif info['tipo_sistema'] == 'infinito':
            if info['num_variables_libres'] == 1:
                contenido.append("• Las ecuaciones definen una línea (infinitos puntos)")
            elif info['num_variables_libres'] == 2:
                contenido.append("• Las ecuaciones definen un plano (infinitos puntos)")
            else:
                contenido.append(f"• Las ecuaciones definen un hiperplano de dimensión {info['num_variables_libres']}")
        else:
            contenido.append("• Las ecuaciones son contradictorias (no hay intersección)")
        
        contenido.append("")
        contenido.append("═" * 60)
        contenido.append("ANÁLISIS COMPLETADO")
        contenido.append("═" * 60)
        
        self.texto_detalle_eq.insert(tk.END, "\n".join(contenido))
    
    def mostrar_informacion_gauss(self, solucionador):
        """Muestra información detallada para el método de Gauss."""
        
        self.texto_detalle_eq.delete(1.0, tk.END)
        
        contenido = []
        contenido.append("═" * 60)
        contenido.append("INFORMACIÓN DETALLADA - MÉTODO GAUSS")
        contenido.append("═" * 60)
        contenido.append("")
        
        # Obtener información del sistema
        if hasattr(solucionador, 'get_solution_info'):
            info_sistema = solucionador.get_solution_info()
            contenido.append("INFORMACIÓN DEL SISTEMA:")
            contenido.append("─" * 30)
            for linea in info_sistema.split('\n'):
                contenido.append(f"• {linea}")
            contenido.append("")
        
        # Análisis del método
        contenido.append("CARACTERÍSTICAS DEL MÉTODO:")
        contenido.append("─" * 30)
        contenido.append("• Método: Eliminación Gaussiana")
        contenido.append("• Proceso: Escalonamiento hacia adelante")
        contenido.append("• Resultado: Matriz en forma escalonada")
        contenido.append("• Resolución: Sustitución hacia atrás")
        contenido.append("")
        
        contenido.append("EFICIENCIA COMPUTACIONAL:")
        contenido.append("─" * 30)
        contenido.append("• Complejidad: O(n³/3) operaciones")
        contenido.append("• Ventaja: Menor número de operaciones que Gauss-Jordan")
        contenido.append("• Desventaja: Requiere sustitución hacia atrás")
        contenido.append("• Uso recomendado: Sistemas con solución única")
        contenido.append("")
        
        contenido.append("CONSIDERACIONES TÉCNICAS:")
        contenido.append("─" * 30)
        contenido.append("• Estabilidad numérica: Buena con pivoteo parcial")
        contenido.append("• Precisión: Limitada por aritmética de punto flotante")
        contenido.append("• Condición: Sensible a matrices mal condicionadas")
        contenido.append("• Pivoteo: Mejora la estabilidad numérica")
        contenido.append("")
        
        contenido.append("═" * 60)
        contenido.append("ANÁLISIS COMPLETADO")
        contenido.append("═" * 60)
        
        self.texto_detalle_eq.insert(tk.END, "\n".join(contenido))
    
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
    
    # ==================== INTERFAZ DE INDEPENDENCIA LINEAL ====================
    
    def crear_interfaz_independencia(self, panel_izq, panel_der):
        """Crea la interfaz completa para independencia lineal."""
        
        self.crear_panel_config_independencia(panel_izq)
        self.crear_panel_vectores(panel_izq)
        self.crear_panel_botones_independencia(panel_izq)
        self.crear_panel_resultados_independencia(panel_der)
    
    def crear_panel_config_independencia(self, padre):
        """Panel de configuración para independencia lineal."""
        
        # Título
        titulo_frame = tk.Frame(padre, bg='#3498db', relief='raised', bd=2)
        titulo_frame.pack(fill='x', pady=(0, 15))
        
        titulo_label = tk.Label(
            titulo_frame,
            text="🏁 ANÁLISIS DE INDEPENDENCIA LINEAL",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#3498db',
            pady=10
        )
        titulo_label.pack()
        
        # Panel de configuración
        config_frame = tk.LabelFrame(padre, text=" ⚙️ Configuración ", font=('Arial', 11, 'bold'))
        config_frame.pack(fill='x', pady=(0, 15))
        
        # Número de vectores
        vectores_frame = tk.Frame(config_frame)
        vectores_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(vectores_frame, text="Número de vectores:", font=('Arial', 10)).pack(side='left')
        
        vectores_spin = tk.Spinbox(
            vectores_frame,
            from_=2, to=6,
            textvariable=self.num_vectores_var,
            width=5,
            command=self.actualizar_matriz_vectores,
            font=('Arial', 10)
        )
        vectores_spin.pack(side='right')
        
        # Dimensión de vectores
        dimension_frame = tk.Frame(config_frame)
        dimension_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(dimension_frame, text="Dimensión de vectores:", font=('Arial', 10)).pack(side='left')
        
        dimension_spin = tk.Spinbox(
            dimension_frame,
            from_=2, to=6,
            textvariable=self.dimension_var,
            width=5,
            command=self.actualizar_matriz_vectores,
            font=('Arial', 10)
        )
        dimension_spin.pack(side='right')
    
    def crear_panel_vectores(self, padre):
        """Panel para entrada de vectores."""
        
        vectores_frame = tk.LabelFrame(padre, text=" 📊 Vectores de Análisis ", font=('Arial', 11, 'bold'))
        vectores_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Canvas para scroll
        self.canvas_vectores = tk.Canvas(vectores_frame, height=200)
        scrollbar_vectores = ttk.Scrollbar(vectores_frame, orient='vertical', command=self.canvas_vectores.yview)
        self.frame_scroll_vectores = tk.Frame(self.canvas_vectores)
        
        self.canvas_vectores.configure(yscrollcommand=scrollbar_vectores.set)
        self.canvas_vectores.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar_vectores.pack(side='right', fill='y')
        
        self.canvas_vectores.create_window((0, 0), window=self.frame_scroll_vectores, anchor='nw')
        self.frame_scroll_vectores.bind('<Configure>',
                                      lambda e: self.canvas_vectores.configure(scrollregion=self.canvas_vectores.bbox('all')))
        
        # Crear matriz inicial
        self.actualizar_matriz_vectores()
    
    def crear_panel_botones_independencia(self, padre):
        """Panel de botones para independencia lineal."""
        
        botones_frame = tk.Frame(padre)
        botones_frame.pack(fill='x', pady=(0, 15))
        
        # Botón analizar
        btn_analizar = tk.Button(
            botones_frame,
            text="🔍 ANALIZAR VECTORES",
            command=self.analizar_independencia,
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            height=2,
            cursor='hand2'
        )
        btn_analizar.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        # Botón limpiar
        btn_limpiar = tk.Button(
            botones_frame,
            text="🧼 LIMPIAR",
            command=self.limpiar_independencia,
            font=('Arial', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            height=2,
            cursor='hand2'
        )
        btn_limpiar.pack(side='right', padx=(5, 0))
        
        # Botón ejemplo
        btn_ejemplo = tk.Button(
            botones_frame,
            text="🎆 EJEMPLO",
            command=self.ejemplo_independencia,
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            height=2,
            cursor='hand2'
        )
        btn_ejemplo.pack(side='right', padx=(5, 0))
    
    def crear_panel_resultados_independencia(self, padre):
        """Panel de resultados para independencia lineal."""
        
        # Notebook para diferentes tipos de resultados
        resultado_notebook = ttk.Notebook(padre)
        resultado_notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Análisis Principal
        tab_analisis = tk.Frame(resultado_notebook, bg=self.colores['fondo'])
        resultado_notebook.add(tab_analisis, text="📊 Análisis")
        
        self.texto_analisis_ind = scrolledtext.ScrolledText(
            tab_analisis,
            wrap=tk.WORD,
            width=70,
            height=25,
            font=('Consolas', 10),
            bg='#f8f9fa',
            fg='#2c3e50'
        )
        self.texto_analisis_ind.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 2: Proceso Paso a Paso
        tab_proceso = tk.Frame(resultado_notebook, bg=self.colores['fondo'])
        resultado_notebook.add(tab_proceso, text="🔄 Proceso")
        
        self.texto_proceso_ind = scrolledtext.ScrolledText(
            tab_proceso,
            wrap=tk.WORD,
            width=70,
            height=25,
            font=('Consolas', 9),
            bg='#fff8e1',
            fg='#2c3e50'
        )
        self.texto_proceso_ind.pack(fill='both', expand=True, padx=10, pady=10)
    
    def actualizar_matriz_vectores(self):
        """Actualiza la matriz de entrada de vectores."""
        
        # Limpiar frame anterior
        for widget in self.frame_scroll_vectores.winfo_children():
            widget.destroy()
        
        num_vectores = int(self.num_vectores_var.get())
        dimension = int(self.dimension_var.get())
        
        self.entradas_vectores = []
        
        # Crear encabezados de columnas
        header_frame = tk.Frame(self.frame_scroll_vectores)
        header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(header_frame, text="", width=10).pack(side='left')  # Espacio para etiquetas de filas
        
        for j in range(num_vectores):
            label = tk.Label(header_frame, text=f"v{j+1}", font=('Arial', 10, 'bold'), width=10)
            label.pack(side='left', padx=2)
        
        # Crear las entradas para cada fila
        for i in range(dimension):
            fila_frame = tk.Frame(self.frame_scroll_vectores)
            fila_frame.pack(fill='x', pady=2)
            
            # Etiqueta de fila
            row_label = tk.Label(fila_frame, text=f"Comp {i+1}:", font=('Arial', 10), width=10)
            row_label.pack(side='left')
            
            fila_entradas = []
            for j in range(num_vectores):
                entrada = tk.Entry(fila_frame, width=10, font=('Arial', 10), justify='center')
                entrada.pack(side='left', padx=2)
                entrada.insert(0, "0")
                fila_entradas.append(entrada)
            
            self.entradas_vectores.append(fila_entradas)
        
        # Actualizar el scroll region
        self.frame_scroll_vectores.update_idletasks()
        self.canvas_vectores.configure(scrollregion=self.canvas_vectores.bbox('all'))
    
    def analizar_independencia(self):
        """Analiza la independencia lineal de los vectores."""
        
        try:
            # Obtener vectores
            vectores = self.obtener_vectores()
            
            # Realizar análisis
            resultado = self.analizador_independencia.analizar_vectores(vectores)
            
            # Mostrar resultados
            self.mostrar_resultados_independencia(resultado)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def obtener_vectores(self):
        """Obtiene la matriz de vectores de las entradas."""
        
        try:
            dimension = len(self.entradas_vectores)
            num_vectores = len(self.entradas_vectores[0])
            
            vectores = np.zeros((dimension, num_vectores))
            
            for i in range(dimension):
                for j in range(num_vectores):
                    valor = self.entradas_vectores[i][j].get().strip()
                    vectores[i, j] = float(valor if valor else '0')
            
            return vectores
            
        except ValueError:
            raise ValueError("Error al leer valores. Verifique que sean números válidos.")
    
    def mostrar_resultados_independencia(self, resultado):
        """Muestra los resultados del análisis de independencia lineal."""
        
        # Limpiar textos anteriores
        self.texto_analisis_ind.delete(1.0, tk.END)
        self.texto_proceso_ind.delete(1.0, tk.END)
        
        # Mostrar reporte completo
        reporte = self.analizador_independencia.obtener_reporte_completo()
        self.texto_analisis_ind.insert(tk.END, reporte)
        
        # Mostrar proceso paso a paso si está disponible
        if resultado.get('pasos_reduccion'):
            proceso_texto = []
            proceso_texto.append("═" * 70)
            proceso_texto.append("PROCESO DE REDUCCIÓN POR FILAS")
            proceso_texto.append("═" * 70)
            proceso_texto.append("")
            
            for i, (matriz_paso, descripcion) in enumerate(resultado['pasos_reduccion'], 1):
                proceso_texto.append(f"PASO {i}: {descripcion}")
                proceso_texto.append("─" * 50)
                
                # Formatear matriz
                for fila in matriz_paso:
                    fila_str = "  ["
                    for valor in fila:
                        fila_str += f" {valor:8.3f}"
                    fila_str += " ]"
                    proceso_texto.append(fila_str)
                
                proceso_texto.append("")
            
            self.texto_proceso_ind.insert(tk.END, "\n".join(proceso_texto))
    
    def limpiar_independencia(self):
        """Limpia la interfaz de independencia lineal."""
        
        for fila in self.entradas_vectores:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        
        self.texto_analisis_ind.delete(1.0, tk.END)
        self.texto_proceso_ind.delete(1.0, tk.END)
    
    def ejemplo_independencia(self):
        """Carga un ejemplo para independencia lineal."""
        
        # Ejemplo: 3 vectores en R3 (linealmente independientes)
        self.num_vectores_var.set("3")
        self.dimension_var.set("3")
        self.actualizar_matriz_vectores()
        
        # Vectores ejemplo: [1,0,0], [0,1,0], [1,1,1]
        valores = [[1, 0, 1], [0, 1, 1], [0, 0, 1]]
        
        for i in range(3):
            for j in range(3):
                self.entradas_vectores[i][j].delete(0, tk.END)
                self.entradas_vectores[i][j].insert(0, str(valores[i][j]))
        
        messagebox.showinfo("Ejemplo", "Ejemplo de vectores independientes cargado")


def main():
    """Función principal."""
    root = tk.Tk()
    app = SistemaUnificado(root)
    root.mainloop()


if __name__ == "__main__":
    main()
