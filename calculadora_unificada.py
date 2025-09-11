#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from gauss_elimination_mejorado import GaussEliminationMejorado
from gauss_jordan import GaussJordan

class CalculadoraUnificada:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Algebra - Sistema Completo")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables del sistema
        self.matriz_entries = []
        self.vector_entries = []
        self.metodo_var = tk.StringVar(value="gauss")
        self.m_var = tk.StringVar(value="3")  # Ecuaciones
        self.n_var = tk.StringVar(value="3")  # Variables
        
        # Solvers
        self.solver_gauss = GaussEliminationMejorado()
        self.solver_jordan = GaussJordan()
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz principal."""
        # Titulo
        titulo_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        titulo_frame.pack(fill='x')
        titulo_frame.pack_propagate(False)
        
        titulo_label = tk.Label(
            titulo_frame, 
            text="Calculadora de Sistemas de Ecuaciones Lineales",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        titulo_label.pack(expand=True)
        
        # Frame principal con dos columnas
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Configuracion del grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuracion y entrada
        panel_izquierdo = tk.Frame(main_frame, bg='#f0f0f0')
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        
        # Panel derecho - Resultados
        panel_derecho = tk.Frame(main_frame, bg='#f0f0f0')
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_panel_configuracion(panel_izquierdo)
        self.crear_panel_matriz(panel_izquierdo)
        self.crear_panel_botones(panel_izquierdo)
        self.crear_panel_resultados(panel_derecho)
    
    def crear_panel_configuracion(self, parent):
        """Crea el panel de configuracion del sistema."""
        config_frame = tk.LabelFrame(parent, text="Configuracion del Sistema", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Frame interno
        inner_frame = tk.Frame(config_frame, bg='#f0f0f0')
        inner_frame.pack(fill='x', padx=10, pady=10)
        
        # Dimensiones
        tk.Label(inner_frame, text="Ecuaciones (m):", bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        tk.Spinbox(inner_frame, from_=1, to=8, textvariable=self.m_var, 
                  width=5).grid(row=0, column=1, padx=5)
        
        tk.Label(inner_frame, text="Variables (n):", bg='#f0f0f0').grid(row=0, column=2, sticky='w', padx=(20,0))
        tk.Spinbox(inner_frame, from_=1, to=8, textvariable=self.n_var, 
                  width=5).grid(row=0, column=3, padx=5)
        
        tk.Button(inner_frame, text="Actualizar Matriz", command=self.crear_matriz,
                 bg='#3498db', fg='white').grid(row=0, column=4, padx=(20,0))
        
        # Metodo
        metodo_frame = tk.Frame(inner_frame, bg='#f0f0f0')
        metodo_frame.grid(row=1, column=0, columnspan=5, sticky='w', pady=(10,0))
        
        tk.Label(metodo_frame, text="Metodo:", bg='#f0f0f0').pack(side='left')
        
        tk.Radiobutton(metodo_frame, text="Gauss (Triangular)", 
                      variable=self.metodo_var, value="gauss",
                      bg='#f0f0f0').pack(side='left', padx=(10,0))
        
        tk.Radiobutton(metodo_frame, text="Gauss-Jordan (Forma Reducida)", 
                      variable=self.metodo_var, value="jordan",
                      bg='#f0f0f0').pack(side='left', padx=(10,0))
    
    def crear_panel_matriz(self, parent):
        """Crea el panel de entrada de la matriz."""
        self.matrix_frame = tk.LabelFrame(parent, text="Sistema de Ecuaciones", 
                                        font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.matrix_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.crear_matriz()
    
    def crear_matriz(self):
        """Crea la interfaz de entrada de la matriz."""
        try:
            m = int(self.m_var.get())
            n = int(self.n_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese numeros validos para las dimensiones")
            return
        
        if m < 1 or n < 1 or m > 8 or n > 8:
            messagebox.showerror("Error", "Las dimensiones deben estar entre 1 y 8")
            return
        
        # Limpiar frame anterior
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        # Informacion del sistema
        info_text = self.determinar_tipo_sistema(m, n)
        info_label = tk.Label(self.matrix_frame, text=f"Sistema {m}x{n} - {info_text}", 
                            font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#f0f0f0')
        info_label.pack(pady=5)
        
        # Frame para las entradas
        entry_frame = tk.Frame(self.matrix_frame, bg='#f0f0f0')
        entry_frame.pack(padx=10, pady=10)
        
        # Crear entradas
        self.matriz_entries = []
        for i in range(m):
            fila = []
            for j in range(n):
                entry = tk.Entry(entry_frame, width=8, justify='center')
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            
            # Simbolo =
            tk.Label(entry_frame, text="=", font=('Arial', 12, 'bold'),
                    bg='#f0f0f0').grid(row=i, column=n, padx=(10, 5))
            
            # Vector independiente
            vector_entry = tk.Entry(entry_frame, width=8, justify='center', bg='#e8f8f5')
            vector_entry.grid(row=i, column=n+1, padx=2, pady=2)
            vector_entry.insert(0, "0")
            fila.append(vector_entry)
            
            self.matriz_entries.append(fila)
        
        # Etiquetas de variables
        var_text = " + ".join([f"x{i+1}" for i in range(n)]) + " = b"
        tk.Label(self.matrix_frame, text=f"Variables: {var_text}", 
                font=('Arial', 9), fg='#7f8c8d', bg='#f0f0f0').pack(pady=(10, 0))
    
    def determinar_tipo_sistema(self, m, n):
        """Determina el tipo de sistema segun las dimensiones."""
        if m > n:
            return "SOBREDETERMINADO"
        elif m < n:
            return "SUBDETERMINADO"
        else:
            return "CUADRADO"
    
    def crear_panel_botones(self, parent):
        """Crea el panel de botones de accion."""
        button_frame = tk.Frame(parent, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(button_frame, text="Resolver Sistema", command=self.resolver_sistema,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        tk.Button(button_frame, text="Limpiar", command=self.limpiar,
                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame, text="Ejemplo", command=self.cargar_ejemplo,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left')
    
    def crear_panel_resultados(self, parent):
        """Crea el panel de resultados con pestanas."""
        self.result_frame = tk.LabelFrame(parent, text="Resultados", 
                                        font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.result_frame.pack(fill='both', expand=True)
        
        # Notebook para organizar resultados
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestana de analisis
        analisis_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(analisis_frame, text="Analisis del Sistema")
        
        self.analisis_text = scrolledtext.ScrolledText(
            analisis_frame, height=20, font=('Courier New', 10),
            bg='white', fg='black'
        )
        self.analisis_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Pestana de proceso
        proceso_frame = tk.Frame(self.notebook, bg='white')
        self.notebook.add(proceso_frame, text="Proceso Paso a Paso")
        
        self.proceso_text = scrolledtext.ScrolledText(
            proceso_frame, height=20, font=('Courier New', 10),
            bg='white', fg='black'
        )
        self.proceso_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def obtener_matriz_y_vector(self):
        """Obtiene la matriz de coeficientes y vector independiente."""
        try:
            m = len(self.matriz_entries)
            n = len(self.matriz_entries[0]) - 1
            
            matriz = np.zeros((m, n))
            for i in range(m):
                for j in range(n):
                    valor = self.matriz_entries[i][j].get().strip()
                    if valor == '':
                        valor = '0'
                    matriz[i, j] = float(valor)
            
            vector = np.zeros(m)
            for i in range(m):
                valor = self.matriz_entries[i][n].get().strip()
                if valor == '':
                    valor = '0'
                vector[i] = float(valor)
            
            return matriz, vector
            
        except ValueError:
            raise ValueError("Error al leer valores. Verifique que todos sean numeros validos.")
    
    def resolver_sistema(self):
        """Resuelve el sistema usando el metodo seleccionado."""
        try:
            matriz, vector = self.obtener_matriz_y_vector()
            
            if self.metodo_var.get() == "jordan":
                solver = self.solver_jordan
                solucion, es_unica, mensaje = solver.resolver(matriz, vector)
            else:
                solver = self.solver_gauss
                solucion, es_unica, mensaje = solver.solve(matriz, vector)
            
            self.mostrar_analisis(matriz, vector, solucion, es_unica, mensaje, solver)
            self.mostrar_proceso(solver)
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_analisis(self, matriz, vector, solucion, es_unica, mensaje, solver):
        """Muestra el analisis completo del sistema."""
        self.analisis_text.delete(1.0, tk.END)
        
        resultado = []
        resultado.append("ANALISIS COMPLETO DEL SISTEMA")
        resultado.append("=" * 50)
        resultado.append("")
        
        # Informacion basica
        m, n = matriz.shape
        resultado.append(f"Sistema: {m} ecuaciones, {n} variables")
        resultado.append(f"Tipo: {self.determinar_tipo_sistema(m, n)}")
        resultado.append(f"Metodo utilizado: {'Gauss-Jordan' if self.metodo_var.get() == 'jordan' else 'Gauss'}")
        resultado.append("")
        
        # Sistema original
        resultado.append("SISTEMA ORIGINAL:")
        resultado.append("-" * 30)
        for i in range(m):
            ecuacion = []
            for j in range(n):
                coef = matriz[i, j]
                if j == 0:
                    ecuacion.append(f"{coef:.2f}x{j+1}")
                else:
                    signo = "+" if coef >= 0 else "-"
                    ecuacion.append(f"{signo} {abs(coef):.2f}x{j+1}")
            
            resultado.append(f"{' '.join(ecuacion)} = {vector[i]:.2f}")
        resultado.append("")
        
        # Analisis detallado para Gauss-Jordan
        if self.metodo_var.get() == "jordan" and hasattr(solver, 'obtener_informacion_detallada'):
            info = solver.obtener_informacion_detallada()
            resultado.append("ANALISIS DETALLADO:")
            resultado.append("-" * 30)
            resultado.append(f"Tipo de sistema: {info['tipo_sistema'].upper()}")
            resultado.append(f"Rango de matriz: {info['rango_matriz']}")
            resultado.append(f"Rango de matriz aumentada: {info['rango_aumentada']}")
            resultado.append(f"Columnas pivote: {info['columnas_pivote']}")
            
            if info['variables_libres']:
                resultado.append(f"Variables libres: {info['variables_libres']} ({info['num_variables_libres']} variables)")
            else:
                resultado.append("Variables libres: Ninguna")
            
            resultado.append(f"Sistema consistente: {'Si' if info['es_consistente'] else 'No'}")
            resultado.append("")
        
        # Resultado
        resultado.append("RESULTADO:")
        resultado.append("-" * 30)
        resultado.append(mensaje)
        resultado.append("")
        
        if solucion is not None:
            resultado.append("SOLUCION:")
            resultado.append("-" * 30)
            if not es_unica:
                resultado.append("(Solucion particular con variables libres = 0)")
            
            for i, val in enumerate(solucion):
                resultado.append(f"x{i+1} = {val:.2f}")
            
            # Verificacion
            resultado.append("")
            resultado.append("VERIFICACION:")
            resultado.append("-" * 30)
            verificacion = np.dot(matriz, solucion)
            for i in range(len(vector)):
                error = abs(verificacion[i] - vector[i])
                estado = "✓" if error < 1e-10 else "~"
                resultado.append(f"Ecuacion {i+1}: {verificacion[i]:.2f} = {vector[i]:.2f} {estado}")
        
        self.analisis_text.insert(tk.END, "\n".join(resultado))
    
    def mostrar_proceso(self, solver):
        """Muestra el proceso paso a paso."""
        self.proceso_text.delete(1.0, tk.END)
        
        contenido = []
        contenido.append("PROCESO PASO A PASO")
        contenido.append("=" * 50)
        contenido.append("")
        
        if hasattr(solver, 'obtener_pasos'):
            pasos = solver.obtener_pasos()
        else:
            pasos = solver.get_steps()
        
        for i, (matriz, operacion) in enumerate(pasos):
            contenido.append(f"PASO {i+1}: {operacion}")
            contenido.append("-" * 40)
            
            if hasattr(solver, 'formatear_matriz'):
                contenido.append(solver.formatear_matriz(matriz))
            else:
                contenido.append(solver.format_matrix(matriz))
            
            contenido.append("")
        
        self.proceso_text.insert(tk.END, "\n".join(contenido))
    
    def limpiar(self):
        """Limpia todos los campos y resultados."""
        for fila in self.matriz_entries:
            for entry in fila:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        
        self.analisis_text.delete(1.0, tk.END)
        self.proceso_text.delete(1.0, tk.END)
    
    def cargar_ejemplo(self):
        """Carga un ejemplo segun el tipo de sistema."""
        m = int(self.m_var.get())
        n = int(self.n_var.get())
        
        ejemplos = {
            (2, 2): {"matriz": [[2, 3], [1, -1]], "vector": [8, 1]},
            (3, 3): {"matriz": [[2, 1, -1], [1, -1, 2], [3, 2, 1]], "vector": [8, 0, 11]},
            (3, 2): {"matriz": [[1, 2], [2, 1], [1, 1]], "vector": [5, 4, 3]},
            (2, 3): {"matriz": [[1, 2, 3], [2, 1, 1]], "vector": [6, 4]},
        }
        
        if (m, n) in ejemplos:
            ejemplo = ejemplos[(m, n)]
            for i in range(m):
                for j in range(n):
                    self.matriz_entries[i][j].delete(0, tk.END)
                    self.matriz_entries[i][j].insert(0, str(ejemplo["matriz"][i][j]))
                
                self.matriz_entries[i][n].delete(0, tk.END)
                self.matriz_entries[i][n].insert(0, str(ejemplo["vector"][i]))
            
            messagebox.showinfo("Ejemplo Cargado", f"Se cargo un ejemplo {m}x{n}")
        else:
            messagebox.showinfo("Ejemplo", "No hay ejemplo predefinido para estas dimensiones")

def main():
    """Funcion principal."""
    root = tk.Tk()
    app = CalculadoraUnificada(root)
    root.mainloop()

if __name__ == "__main__":
    main()
