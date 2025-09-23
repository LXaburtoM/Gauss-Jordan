#!/usr/bin/env python3
"""
Operaciones Matriciales - Suma y Multiplicación de Matrices
Interfaz gráfica para realizar operaciones básicas con matrices
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np

class OperacionesMatriciales:
    """
    Interfaz gráfica para operaciones con matrices: suma y multiplicación.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones Matriciales - Suma y Multiplicación")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Variables para las matrices
        self.entradas_matriz_a = []
        self.entradas_matriz_b = []
        self.operacion_var = tk.StringVar(value="suma")
        self.filas_a_var = tk.StringVar(value="3")
        self.columnas_a_var = tk.StringVar(value="3")
        self.filas_b_var = tk.StringVar(value="3")
        self.columnas_b_var = tk.StringVar(value="3")
        
        # Colores del tema
        self.colores = {
            'primario': '#2c3e50',
            'secundario': '#3498db',
            'exito': '#27ae60',
            'advertencia': '#f39c12',
            'error': '#e74c3c',
            'fondo': '#f0f0f0',
            'blanco': '#ffffff',
            'texto': '#2c3e50'
        }
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz principal."""
        
        # Título principal
        titulo_frame = tk.Frame(self.root, bg=self.colores['primario'], height=70)
        titulo_frame.pack(fill='x')
        titulo_frame.pack_propagate(False)
        
        titulo_label = tk.Label(
            titulo_frame, 
            text="🧮 OPERACIONES MATRICIALES - SUMA Y MULTIPLICACIÓN 🧮",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg=self.colores['primario']
        )
        titulo_label.pack(expand=True)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configurar grid principal
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y matrices
        panel_izquierdo = tk.Frame(frame_principal, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultado
        panel_derecho = tk.Frame(frame_principal, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_panel_configuracion(panel_izquierdo)
        self.crear_panel_matrices(panel_izquierdo)
        self.crear_panel_botones(panel_izquierdo)
        self.crear_panel_resultado(panel_derecho)
    
    def crear_panel_configuracion(self, padre):
        """Crea el panel de configuración de operaciones."""
        
        config_frame = tk.LabelFrame(
            padre, 
            text="⚙️ Configuración de Operación", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Frame interno
        frame_interno = tk.Frame(config_frame, bg=self.colores['fondo'])
        frame_interno.pack(fill='x', padx=15, pady=15)
        
        # Tipo de operación
        tk.Label(
            frame_interno, 
            text="Operación:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=0, sticky='w', columnspan=2)
        
        tk.Radiobutton(
            frame_interno, 
            text="➕ Suma de Matrices (A + B)", 
            variable=self.operacion_var, 
            value="suma",
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            command=self.cambiar_operacion
        ).grid(row=1, column=0, sticky='w', columnspan=2, padx=(20, 0))
        
        tk.Radiobutton(
            frame_interno, 
            text="✖️ Multiplicación de Matrices (A × B)", 
            variable=self.operacion_var, 
            value="multiplicacion",
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            command=self.cambiar_operacion
        ).grid(row=2, column=0, sticky='w', columnspan=2, padx=(20, 0))
        
        # Dimensiones de matrices
        tk.Label(
            frame_interno, 
            text="Dimensiones:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold')
        ).grid(row=3, column=0, sticky='w', columnspan=2, pady=(15, 5))
        
        # Matriz A
        tk.Label(
            frame_interno, 
            text="Matriz A - Filas:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=4, column=0, sticky='w')
        
        tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=6, 
            textvariable=self.filas_a_var, 
            width=5,
            font=('Arial', 10)
        ).grid(row=4, column=1, padx=5)
        
        tk.Label(
            frame_interno, 
            text="Columnas:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=4, column=2, sticky='w', padx=(20, 0))
        
        tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=6, 
            textvariable=self.columnas_a_var, 
            width=5,
            font=('Arial', 10)
        ).grid(row=4, column=3, padx=5)
        
        # Matriz B
        tk.Label(
            frame_interno, 
            text="Matriz B - Filas:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=5, column=0, sticky='w')
        
        self.filas_b_spin = tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=6, 
            textvariable=self.filas_b_var, 
            width=5,
            font=('Arial', 10)
        )
        self.filas_b_spin.grid(row=5, column=1, padx=5)
        
        tk.Label(
            frame_interno, 
            text="Columnas:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=5, column=2, sticky='w', padx=(20, 0))
        
        self.columnas_b_spin = tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=6, 
            textvariable=self.columnas_b_var, 
            width=5,
            font=('Arial', 10)
        )
        self.columnas_b_spin.grid(row=5, column=3, padx=5)
        
        # Botón actualizar
        tk.Button(
            frame_interno, 
            text="Actualizar Matrices", 
            command=self.actualizar_matrices,
            bg=self.colores['secundario'], 
            fg='white',
            font=('Arial', 10, 'bold')
        ).grid(row=6, column=0, columnspan=4, pady=(15, 0))
    
    def crear_panel_matrices(self, padre):
        """Crea el panel de entrada de matrices."""
        
        self.frame_matrices = tk.LabelFrame(
            padre, 
            text="📊 Entrada de Matrices", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        self.frame_matrices.pack(fill='both', expand=True, pady=(0, 10))
        
        self.actualizar_matrices()
    
    def actualizar_matrices(self):
        """Actualiza la interfaz de entrada de matrices."""
        
        try:
            filas_a = int(self.filas_a_var.get())
            cols_a = int(self.columnas_a_var.get())
            filas_b = int(self.filas_b_var.get())
            cols_b = int(self.columnas_b_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos para las dimensiones")
            return
        
        # Limpiar frame anterior
        for widget in self.frame_matrices.winfo_children():
            widget.destroy()
        
        # Crear frame con scroll
        canvas = tk.Canvas(self.frame_matrices, bg=self.colores['fondo'])
        scrollbar = ttk.Scrollbar(self.frame_matrices, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colores['fondo'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Matriz A
        tk.Label(
            scrollable_frame, 
            text=f"Matriz A ({filas_a}×{cols_a})", 
            font=('Arial', 11, 'bold'), 
            fg=self.colores['secundario'], 
            bg=self.colores['fondo']
        ).pack(pady=(10, 5))
        
        frame_a = tk.Frame(scrollable_frame, bg=self.colores['fondo'])
        frame_a.pack(pady=5)
        
        self.entradas_matriz_a = []
        for i in range(filas_a):
            fila = []
            for j in range(cols_a):
                entrada = tk.Entry(frame_a, width=8, justify='center', font=('Arial', 10))
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            self.entradas_matriz_a.append(fila)
        
        # Matriz B
        tk.Label(
            scrollable_frame, 
            text=f"Matriz B ({filas_b}×{cols_b})", 
            font=('Arial', 11, 'bold'), 
            fg=self.colores['secundario'], 
            bg=self.colores['fondo']
        ).pack(pady=(20, 5))
        
        frame_b = tk.Frame(scrollable_frame, bg=self.colores['fondo'])
        frame_b.pack(pady=5)
        
        self.entradas_matriz_b = []
        for i in range(filas_b):
            fila = []
            for j in range(cols_b):
                entrada = tk.Entry(frame_b, width=8, justify='center', font=('Arial', 10))
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            self.entradas_matriz_b.append(fila)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def cambiar_operacion(self):
        """Ajusta las dimensiones según la operación seleccionada."""
        
        if self.operacion_var.get() == "suma":
            # Para suma, las matrices deben tener las mismas dimensiones
            self.filas_b_var.set(self.filas_a_var.get())
            self.columnas_b_var.set(self.columnas_a_var.get())
            self.filas_b_spin.configure(state='disabled')
            self.columnas_b_spin.configure(state='disabled')
        else:
            # Para multiplicación, columnas de A = filas de B
            self.filas_b_spin.configure(state='normal')
            self.columnas_b_spin.configure(state='normal')
    
    def crear_panel_botones(self, padre):
        """Crea el panel de botones de acción."""
        
        botones_frame = tk.Frame(padre, bg=self.colores['fondo'])
        botones_frame.pack(fill='x', pady=(0, 10))
        
        # Botón calcular
        tk.Button(
            botones_frame, 
            text="🚀 CALCULAR OPERACIÓN", 
            command=self.calcular_operacion,
            bg=self.colores['exito'], 
            fg='white', 
            font=('Arial', 12, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # Botón limpiar
        tk.Button(
            botones_frame, 
            text="🧹 Limpiar", 
            command=self.limpiar_todo,
            bg=self.colores['advertencia'], 
            fg='white', 
            font=('Arial', 11, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        # Botón ejemplo
        tk.Button(
            botones_frame, 
            text="📝 Ejemplo", 
            command=self.cargar_ejemplo,
            bg='#9b59b6', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left')
    
    def crear_panel_resultado(self, padre):
        """Crea el panel de resultados."""
        
        frame_resultado = tk.LabelFrame(
            padre, 
            text="📈 Resultado de la Operación", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        frame_resultado.pack(fill='both', expand=True)
        
        self.texto_resultado = scrolledtext.ScrolledText(
            frame_resultado, 
            height=30, 
            font=('Consolas', 10),
            bg='white', 
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.texto_resultado.pack(fill='both', expand=True, padx=15, pady=15)
    
    def obtener_matrices(self):
        """Obtiene las matrices A y B de las entradas."""
        
        try:
            # Matriz A
            filas_a = len(self.entradas_matriz_a)
            cols_a = len(self.entradas_matriz_a[0])
            matriz_a = np.zeros((filas_a, cols_a))
            
            for i in range(filas_a):
                for j in range(cols_a):
                    valor = self.entradas_matriz_a[i][j].get().strip()
                    if valor == '':
                        valor = '0'
                    matriz_a[i, j] = float(valor)
            
            # Matriz B
            filas_b = len(self.entradas_matriz_b)
            cols_b = len(self.entradas_matriz_b[0])
            matriz_b = np.zeros((filas_b, cols_b))
            
            for i in range(filas_b):
                for j in range(cols_b):
                    valor = self.entradas_matriz_b[i][j].get().strip()
                    if valor == '':
                        valor = '0'
                    matriz_b[i, j] = float(valor)
            
            return matriz_a, matriz_b
            
        except ValueError:
            raise ValueError("Error al leer los valores. Verifique que todos sean números válidos.")
    
    def calcular_operacion(self):
        """Realiza la operación seleccionada."""
        
        try:
            matriz_a, matriz_b = self.obtener_matrices()
            operacion = self.operacion_var.get()
            
            resultado_texto = []
            resultado_texto.append("═" * 60)
            resultado_texto.append("RESULTADO DE OPERACIÓN MATRICIAL")
            resultado_texto.append("═" * 60)
            resultado_texto.append("")
            
            # Mostrar matrices originales
            resultado_texto.append("MATRIZ A:")
            resultado_texto.append("─" * 20)
            resultado_texto.extend(self.formatear_matriz(matriz_a))
            resultado_texto.append("")
            
            resultado_texto.append("MATRIZ B:")
            resultado_texto.append("─" * 20)
            resultado_texto.extend(self.formatear_matriz(matriz_b))
            resultado_texto.append("")
            
            # Realizar operación
            if operacion == "suma":
                if matriz_a.shape != matriz_b.shape:
                    raise ValueError("Para la suma, las matrices deben tener las mismas dimensiones")
                
                resultado = matriz_a + matriz_b
                resultado_texto.append("OPERACIÓN: A + B")
                
            else:  # multiplicación
                if matriz_a.shape[1] != matriz_b.shape[0]:
                    raise ValueError(f"Para la multiplicación, el número de columnas de A ({matriz_a.shape[1]}) "
                                   f"debe ser igual al número de filas de B ({matriz_b.shape[0]})")
                
                resultado = np.dot(matriz_a, matriz_b)
                resultado_texto.append("OPERACIÓN: A × B")
            
            resultado_texto.append("─" * 20)
            resultado_texto.extend(self.formatear_matriz(resultado))
            resultado_texto.append("")
            
            # Información adicional
            resultado_texto.append("INFORMACIÓN:")
            resultado_texto.append("─" * 20)
            resultado_texto.append(f"• Dimensión de A: {matriz_a.shape[0]}×{matriz_a.shape[1]}")
            resultado_texto.append(f"• Dimensión de B: {matriz_b.shape[0]}×{matriz_b.shape[1]}")
            resultado_texto.append(f"• Dimensión del resultado: {resultado.shape[0]}×{resultado.shape[1]}")
            
            if operacion == "suma":
                resultado_texto.append(f"• Suma elemento por elemento")
            else:
                resultado_texto.append(f"• Producto matricial (filas de A × columnas de B)")
            
            resultado_texto.append("")
            resultado_texto.append("═" * 60)
            
            self.texto_resultado.delete(1.0, tk.END)
            self.texto_resultado.insert(tk.END, "\n".join(resultado_texto))
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def formatear_matriz(self, matriz):
        """Formatea una matriz para mostrar."""
        
        filas_formateadas = []
        for fila in matriz:
            elementos = [f"{val:8.2f}" for val in fila]
            filas_formateadas.append("  [" + "  ".join(elementos) + "]")
        return filas_formateadas
    
    def limpiar_todo(self):
        """Limpia todas las entradas y resultados."""
        
        # Limpiar entradas de matriz A
        for fila in self.entradas_matriz_a:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        
        # Limpiar entradas de matriz B
        for fila in self.entradas_matriz_b:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        
        # Limpiar resultado
        self.texto_resultado.delete(1.0, tk.END)
        
        messagebox.showinfo("Limpieza", "Todas las entradas han sido limpiadas")
    
    def cargar_ejemplo(self):
        """Carga un ejemplo según la operación seleccionada."""
        
        operacion = self.operacion_var.get()
        
        if operacion == "suma":
            # Ejemplo de suma 2x2
            self.filas_a_var.set("2")
            self.columnas_a_var.set("2")
            self.filas_b_var.set("2")
            self.columnas_b_var.set("2")
            self.actualizar_matrices()
            
            # Matriz A
            valores_a = [[1, 2], [3, 4]]
            for i in range(2):
                for j in range(2):
                    self.entradas_matriz_a[i][j].delete(0, tk.END)
                    self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))
            
            # Matriz B
            valores_b = [[5, 6], [7, 8]]
            for i in range(2):
                for j in range(2):
                    self.entradas_matriz_b[i][j].delete(0, tk.END)
                    self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))
            
            messagebox.showinfo("Ejemplo Cargado", "Ejemplo de suma de matrices 2×2 cargado")
            
        else:  # multiplicación
            # Ejemplo de multiplicación 2x3 × 3x2
            self.filas_a_var.set("2")
            self.columnas_a_var.set("3")
            self.filas_b_var.set("3")
            self.columnas_b_var.set("2")
            self.actualizar_matrices()
            
            # Matriz A (2×3)
            valores_a = [[1, 2, 3], [4, 5, 6]]
            for i in range(2):
                for j in range(3):
                    self.entradas_matriz_a[i][j].delete(0, tk.END)
                    self.entradas_matriz_a[i][j].insert(0, str(valores_a[i][j]))
            
            # Matriz B (3×2)
            valores_b = [[7, 8], [9, 10], [11, 12]]
            for i in range(3):
                for j in range(2):
                    self.entradas_matriz_b[i][j].delete(0, tk.END)
                    self.entradas_matriz_b[i][j].insert(0, str(valores_b[i][j]))
            
            messagebox.showinfo("Ejemplo Cargado", "Ejemplo de multiplicación 2×3 × 3×2 cargado")


def main():
    """Función principal de la aplicación."""
    root = tk.Tk()
    aplicacion = OperacionesMatriciales(root)
    root.mainloop()


if __name__ == "__main__":
    main()
