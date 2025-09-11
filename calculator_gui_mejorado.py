#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from gauss_elimination_mejorado import GaussEliminationMejorado

class CalculadoraAlgebraGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra - Matrices Rectangulares")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.matriz_entries = []
        self.vector_entries = []
        self.solver = GaussEliminationMejorado()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Título
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🔢 CALCULADORA DE ÁLGEBRA - MATRICES RECTANGULARES",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Panel de configuración
        config_frame = tk.LabelFrame(main_frame, text="Configuración del Sistema", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Selección de dimensiones
        dim_frame = tk.Frame(config_frame, bg='#f0f0f0')
        dim_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(dim_frame, text="Número de ecuaciones (m):", 
                font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=0, sticky='w')
        self.m_var = tk.StringVar(value="3")
        tk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.m_var, 
                  width=5, font=('Arial', 10)).grid(row=0, column=1, padx=(10, 20))
        
        tk.Label(dim_frame, text="Número de incógnitas (n):", 
                font=('Arial', 10), bg='#f0f0f0').grid(row=0, column=2, sticky='w')
        self.n_var = tk.StringVar(value="3")
        tk.Spinbox(dim_frame, from_=1, to=10, textvariable=self.n_var, 
                  width=5, font=('Arial', 10)).grid(row=0, column=3, padx=(10, 20))
        
        tk.Button(dim_frame, text="Crear Matriz", command=self.crear_matriz,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold')).grid(row=0, column=4, padx=(20, 0))
        
        # Frame para la matriz
        self.matrix_frame = tk.LabelFrame(main_frame, text="Sistema de Ecuaciones", 
                                        font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.matrix_frame.pack(fill='x', pady=(0, 10))
        
        # Panel de botones
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill='x', pady=(0, 10))
        
        tk.Button(button_frame, text="🔍 Resolver Sistema", command=self.resolver_sistema,
                 bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame, text="📝 Ver Pasos Detallados", command=self.ver_pasos,
                 bg='#e67e22', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame, text="🧹 Limpiar", command=self.limpiar,
                 bg='#95a5a6', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left', padx=(0, 10))
        
        tk.Button(button_frame, text="📋 Ejemplo", command=self.cargar_ejemplo,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 height=2).pack(side='left')
        
        # Panel de resultados
        self.result_frame = tk.LabelFrame(main_frame, text="Resultados", 
                                        font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.result_frame.pack(fill='both', expand=True)
        
        # Área de texto con scroll
        self.result_text = scrolledtext.ScrolledText(
            self.result_frame, 
            height=15, 
            font=('Courier New', 10),
            bg='white',
            fg='black'
        )
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Crear matriz inicial
        self.crear_matriz()
    
    def crear_matriz(self):
        """Crea la interfaz de entrada de la matriz."""
        try:
            m = int(self.m_var.get())
            n = int(self.n_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos para las dimensiones")
            return
        
        if m < 1 or n < 1 or m > 10 or n > 10:
            messagebox.showerror("Error", "Las dimensiones deben estar entre 1 y 10")
            return
        
        # Limpiar frame anterior
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        # Información del sistema
        info_frame = tk.Frame(self.matrix_frame, bg='#f0f0f0')
        info_frame.pack(fill='x', padx=10, pady=(10, 5))
        
        tipo_sistema = self.determinar_tipo_sistema(m, n)
        tk.Label(info_frame, text=f"Sistema {m}×{n} - {tipo_sistema}", 
                font=('Arial', 10, 'bold'), fg='#2c3e50', bg='#f0f0f0').pack()
        
        # Frame para entradas
        entry_frame = tk.Frame(self.matrix_frame, bg='#f0f0f0')
        entry_frame.pack(padx=10, pady=10)
        
        # Crear entradas para la matriz de coeficientes
        self.matriz_entries = []
        for i in range(m):
            fila = []
            for j in range(n):
                entry = tk.Entry(entry_frame, width=8, justify='center', 
                               font=('Arial', 10))
                entry.grid(row=i, column=j, padx=2, pady=2)
                entry.insert(0, "0")
                fila.append(entry)
            
            # Agregar símbolo =
            tk.Label(entry_frame, text="=", font=('Arial', 12, 'bold'),
                    bg='#f0f0f0').grid(row=i, column=n, padx=(10, 5))
            
            # Entrada para el vector independiente
            vector_entry = tk.Entry(entry_frame, width=8, justify='center',
                                  font=('Arial', 10), bg='#e8f8f5')
            vector_entry.grid(row=i, column=n+1, padx=2, pady=2)
            vector_entry.insert(0, "0")
            fila.append(vector_entry)
            
            self.matriz_entries.append(fila)
        
        # Etiquetas de variables
        var_frame = tk.Frame(self.matrix_frame, bg='#f0f0f0')
        var_frame.pack(pady=(0, 10))
        
        variables_text = " + ".join([f"x{i+1}" for i in range(n)]) + " = b"
        tk.Label(var_frame, text=f"Variables: {variables_text}", 
                font=('Arial', 9), fg='#7f8c8d', bg='#f0f0f0').pack()
    
    def determinar_tipo_sistema(self, m, n):
        """Determina el tipo de sistema según las dimensiones."""
        if m > n:
            return "SOBREDETERMINADO (más ecuaciones que incógnitas)"
        elif m < n:
            return "SUBDETERMINADO (menos ecuaciones que incógnitas)"
        else:
            return "CUADRADO (igual número de ecuaciones e incógnitas)"
    
    def obtener_matriz_y_vector(self):
        """Obtiene la matriz de coeficientes y vector independiente."""
        try:
            m = len(self.matriz_entries)
            n = len(self.matriz_entries[0]) - 1  # -1 porque la última columna es el vector
            
            # Extraer matriz de coeficientes
            matriz = np.zeros((m, n))
            for i in range(m):
                for j in range(n):
                    valor = self.matriz_entries[i][j].get().strip()
                    if valor == '':
                        valor = '0'
                    matriz[i, j] = float(valor)
            
            # Extraer vector independiente
            vector = np.zeros(m)
            for i in range(m):
                valor = self.matriz_entries[i][n].get().strip()  # Última columna
                if valor == '':
                    valor = '0'
                vector[i] = float(valor)
            
            return matriz, vector
            
        except ValueError as e:
            raise ValueError("Error al leer los valores de la matriz. Verifique que todos sean números válidos.")
    
    def resolver_sistema(self):
        """Resuelve el sistema de ecuaciones."""
        try:
            # Obtener datos
            matriz, vector = self.obtener_matriz_y_vector()
            
            # Resolver
            self.solver = GaussEliminationMejorado()
            solucion, tiene_solucion_unica, mensaje = self.solver.solve(matriz, vector)
            
            # Mostrar resultados
            self.mostrar_resultados(matriz, vector, solucion, tiene_solucion_unica, mensaje)
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_resultados(self, matriz, vector, solucion, tiene_solucion_unica, mensaje):
        """Muestra los resultados en el área de texto."""
        self.result_text.delete(1.0, tk.END)
        
        resultado = []
        resultado.append("=" * 80)
        resultado.append("RESULTADOS DE LA RESOLUCIÓN")
        resultado.append("=" * 80)
        
        # Información del sistema
        m, n = matriz.shape
        resultado.append(f"Sistema: {m} ecuaciones, {n} incógnitas")
        resultado.append(f"Tipo: {self.determinar_tipo_sistema(m, n)}")
        resultado.append("")
        
        # Sistema original
        resultado.append("SISTEMA ORIGINAL:")
        resultado.append("-" * 30)
        for i in range(m):
            ecuacion = []
            for j in range(n):
                coef = matriz[i, j]
                if j == 0:
                    if coef >= 0:
                        ecuacion.append(f"{coef:.2f}x{j+1}")
                    else:
                        ecuacion.append(f"{coef:.2f}x{j+1}")
                else:
                    if coef >= 0:
                        ecuacion.append(f"+ {coef:.2f}x{j+1}")
                    else:
                        ecuacion.append(f"- {abs(coef):.2f}x{j+1}")
            
            resultado.append(f"{' '.join(ecuacion)} = {vector[i]:.2f}")
        resultado.append("")
        
        # Resultado
        resultado.append("ANÁLISIS:")
        resultado.append("-" * 30)
        resultado.append(f"Estado: {mensaje}")
        resultado.append("")
        
        if solucion is not None:
            if tiene_solucion_unica:
                resultado.append("✅ SOLUCIÓN ÚNICA:")
            else:
                resultado.append("✅ SOLUCIÓN PARTICULAR (variables libres = 0):")
            
            resultado.append("-" * 30)
            for i, val in enumerate(solucion):
                resultado.append(f"x{i+1} = {val:.2f}")
            
            # Verificación
            resultado.append("")
            resultado.append("VERIFICACIÓN:")
            resultado.append("-" * 30)
            verificacion = np.dot(matriz, solucion)
            for i in range(len(vector)):
                error = abs(verificacion[i] - vector[i])
                if error < 1e-10:
                    resultado.append(f"Ecuación {i+1}: {verificacion[i]:.2f} = {vector[i]:.2f} ✅")
                else:
                    resultado.append(f"Ecuación {i+1}: {verificacion[i]:.2f} ≈ {vector[i]:.2f} (Error: {error:.2e})")
        else:
            resultado.append("❌ NO HAY SOLUCIÓN")
        
        # Información adicional
        steps = self.solver.get_steps()
        resultado.append("")
        resultado.append(f"Pasos de eliminación generados: {len(steps)}")
        resultado.append("(Use 'Ver Pasos Detallados' para ver el proceso completo)")
        
        # Mostrar en el área de texto
        self.result_text.insert(tk.END, "\n".join(resultado))
    
    def ver_pasos(self):
        """Muestra los pasos detallados de la eliminación."""
        if not hasattr(self.solver, 'steps') or not self.solver.steps:
            messagebox.showwarning("Advertencia", "Primero debe resolver un sistema")
            return
        
        # Crear ventana para pasos
        pasos_window = tk.Toplevel(self.root)
        pasos_window.title("Pasos Detallados - Eliminación de Gauss")
        pasos_window.geometry("800x600")
        pasos_window.configure(bg='#f0f0f0')
        
        # Área de texto con scroll
        pasos_text = scrolledtext.ScrolledText(
            pasos_window,
            font=('Courier New', 10),
            bg='white',
            fg='black'
        )
        pasos_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Generar contenido de pasos
        pasos_content = []
        pasos_content.append("PASOS DETALLADOS DE LA ELIMINACIÓN DE GAUSS")
        pasos_content.append("=" * 60)
        pasos_content.append("")
        
        steps = self.solver.get_steps()
        for i, (matriz, operacion) in enumerate(steps):
            pasos_content.append(f"PASO {i+1}: {operacion}")
            pasos_content.append("-" * 50)
            pasos_content.append(self.solver.format_matrix(matriz))
            pasos_content.append("")
        
        pasos_text.insert(tk.END, "\n".join(pasos_content))
    
    def cargar_ejemplo(self):
        """Carga un ejemplo de sistema rectangular."""
        ejemplos = [
            {
                "nombre": "Sistema 3×2 (Sobredeterminado)",
                "m": 3, "n": 2,
                "matriz": [[1, 2], [2, 1], [1, 1]],
                "vector": [5, 4, 3]
            },
            {
                "nombre": "Sistema 2×3 (Subdeterminado)", 
                "m": 2, "n": 3,
                "matriz": [[1, 2, 3], [2, 1, 1]],
                "vector": [6, 4]
            },
            {
                "nombre": "Sistema 4×3 (Sobredeterminado)",
                "m": 4, "n": 3,
                "matriz": [[1, 1, 1], [1, -1, 2], [2, 1, -1], [1, 2, -1]],
                "vector": [6, 2, 3, 5]
            }
        ]
        
        # Seleccionar ejemplo aleatoriamente
        import random
        ejemplo = random.choice(ejemplos)
        
        # Configurar dimensiones
        self.m_var.set(str(ejemplo["m"]))
        self.n_var.set(str(ejemplo["n"]))
        self.crear_matriz()
        
        # Llenar datos
        for i in range(ejemplo["m"]):
            for j in range(ejemplo["n"]):
                self.matriz_entries[i][j].delete(0, tk.END)
                self.matriz_entries[i][j].insert(0, str(ejemplo["matriz"][i][j]))
            
            # Vector independiente
            self.matriz_entries[i][ejemplo["n"]].delete(0, tk.END)
            self.matriz_entries[i][ejemplo["n"]].insert(0, str(ejemplo["vector"][i]))
        
        messagebox.showinfo("Ejemplo Cargado", f"Se cargó: {ejemplo['nombre']}")
    
    def limpiar(self):
        """Limpia todos los campos."""
        for fila in self.matriz_entries:
            for entry in fila:
                entry.delete(0, tk.END)
                entry.insert(0, "0")
        
        self.result_text.delete(1.0, tk.END)

def main():
    """Función principal."""
    root = tk.Tk()
    app = CalculadoraAlgebraGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
