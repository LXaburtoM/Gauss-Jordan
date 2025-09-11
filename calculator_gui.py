import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font as tkFont
import numpy as np
from gauss_elimination import GaussElimination
import math

class AlgebraCalculator:
    """
    Interfaz gráfica para la calculadora de álgebra con método de eliminación de Gauss.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra - Eliminación de Gauss")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Variables
        self.num_equations = tk.StringVar(value="3")
        self.matrix_entries = []
        self.vector_entries = []
        self.gauss_solver = GaussElimination()
        
        self.setup_ui()
        self.create_matrix_inputs()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid weight
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Título
        title_label = ttk.Label(main_frame, text="Calculadora de Sistemas de Ecuaciones Lineales", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=10)
        
        # Frame para número de ecuaciones
        eq_frame = ttk.Frame(main_frame)
        eq_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(eq_frame, text="Número de ecuaciones:").grid(row=0, column=0, padx=5)
        eq_spinbox = ttk.Spinbox(eq_frame, from_=2, to=6, textvariable=self.num_equations, 
                                width=5, command=self.update_matrix_size)
        eq_spinbox.grid(row=0, column=1, padx=5)
        
        ttk.Button(eq_frame, text="Actualizar Matriz", 
                  command=self.update_matrix_size).grid(row=0, column=2, padx=10)
        
        # Frame para la matriz de entrada
        self.matrix_frame = ttk.LabelFrame(main_frame, text="Matriz de Coeficientes y Vector Independiente", 
                                          padding="10")
        self.matrix_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        self.matrix_frame.columnconfigure(0, weight=1)
        
        # Botón resolver
        solve_button = ttk.Button(main_frame, text="Resolver Sistema", 
                                 command=self.solve_system, style="Accent.TButton")
        solve_button.grid(row=3, column=0, pady=10)
        
        # Área de resultados
        results_frame = ttk.LabelFrame(main_frame, text="Resultados y Proceso", padding="10")
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Texto con scroll para mostrar resultados (con scroll mejorado)
        self.results_text = scrolledtext.ScrolledText(results_frame, 
                                                     height=22, 
                                                     width=85, 
                                                     font=("Courier New", 10),
                                                     wrap=tk.WORD,
                                                     borderwidth=2,
                                                     relief='solid')
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        # Frame para botones adicionales
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, pady=5)
        
        ttk.Button(buttons_frame, text="Limpiar Resultados", 
                  command=self.clear_results).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Ejemplo", 
                  command=self.load_example).grid(row=0, column=1, padx=5)
    
    def create_matrix_inputs(self):
        """Crea los campos de entrada para la matriz."""
        try:
            n = int(self.num_equations.get())
        except ValueError:
            messagebox.showerror("Error", "Número de ecuaciones debe ser un entero válido.")
            return
        
        # Limpiar entradas anteriores
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        
        self.matrix_entries = []
        self.vector_entries = []
        
        # Crear encabezados
        ttk.Label(self.matrix_frame, text="Matriz de Coeficientes", 
                 font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=n, pady=5)
        ttk.Label(self.matrix_frame, text="Vector\nIndependiente", 
                 font=("Arial", 12, "bold")).grid(row=0, column=n+1, pady=5)
        
        # Variables para las ecuaciones
        var_labels = []
        for i in range(n):
            var_labels.append(f"x{i+1}")
        
        # Crear encabezados de variables
        for j in range(n):
            ttk.Label(self.matrix_frame, text=var_labels[j], 
                     font=("Arial", 10, "bold")).grid(row=1, column=j, padx=2)
        ttk.Label(self.matrix_frame, text="=", font=("Arial", 10, "bold")).grid(row=1, column=n, padx=5)
        ttk.Label(self.matrix_frame, text="b", font=("Arial", 10, "bold")).grid(row=1, column=n+1, padx=2)
        
        # Crear campos de entrada
        for i in range(n):
            row_entries = []
            
            # Etiqueta de ecuación (usar columnspan para colocarla antes de las columnas)
            eq_label = ttk.Label(self.matrix_frame, text=f"Ec. {i+1}:")
            eq_label.grid(row=i+2, column=0, sticky=tk.W, padx=(0, 5))
            
            for j in range(n):
                entry = ttk.Entry(self.matrix_frame, width=10, justify="center")
                entry.grid(row=i+2, column=j, padx=2, pady=2)
                entry.bind('<KeyRelease>', self.validate_numeric_input)
                row_entries.append(entry)
            
            # Símbolo igual
            ttk.Label(self.matrix_frame, text="=").grid(row=i+2, column=n, padx=5)
            
            # Vector independiente
            vector_entry = ttk.Entry(self.matrix_frame, width=10, justify="center")
            vector_entry.grid(row=i+2, column=n+1, padx=2, pady=2)
            vector_entry.bind('<KeyRelease>', self.validate_numeric_input)
            
            self.matrix_entries.append(row_entries)
            self.vector_entries.append(vector_entry)
    
    def update_matrix_size(self):
        """Actualiza el tamaño de la matriz cuando cambia el número de ecuaciones."""
        self.create_matrix_inputs()
        self.clear_results()
    
    def validate_numeric_input(self, event):
        """Valida que la entrada sea numérica."""
        widget = event.widget
        value = widget.get()
        
        if value == "" or value == "-" or value == ".":
            return  # Permitir valores vacíos o en proceso de escritura
        
        try:
            float(value)
            widget.configure(style="TEntry")  # Estilo normal
        except ValueError:
            widget.configure(style="Invalid.TEntry")  # Estilo de error (rojo)
    
    def get_matrix_values(self):
        """Obtiene los valores de la matriz y vector desde los campos de entrada."""
        try:
            n = int(self.num_equations.get())
            matrix = np.zeros((n, n))
            vector = np.zeros(n)
            
            # Obtener valores de la matriz
            for i in range(n):
                for j in range(n):
                    value = self.matrix_entries[i][j].get().strip()
                    if not value:
                        raise ValueError(f"Campo vacío en posición ({i+1}, {j+1})")
                    try:
                        matrix[i, j] = float(value)
                    except ValueError:
                        raise ValueError(f"Valor no numérico en posición ({i+1}, {j+1}): '{value}'")
                
                # Obtener valores del vector
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
    
    def solve_system(self):
        """Resuelve el sistema de ecuaciones y muestra los resultados."""
        # Obtener valores de la matriz
        matrix, vector, valid, error_msg = self.get_matrix_values()
        
        if not valid:
            messagebox.showerror("Error de Entrada", f"Error en los datos ingresados:\n{error_msg}\n\nIngrese únicamente valores numéricos.")
            return
        
        # Resolver el sistema
        solution, has_unique_solution, error_msg = self.gauss_solver.solve(matrix, vector)
        
        # Limpiar área de resultados
        self.results_text.delete('1.0', tk.END)
        
        if not has_unique_solution:
            messagebox.showerror("Error", error_msg)
            self.results_text.insert(tk.END, f"ERROR: {error_msg}\n\n")
            return
        
        # Mostrar sistema original
        self.results_text.insert(tk.END, "SISTEMA DE ECUACIONES ORIGINAL:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        n = len(matrix)
        for i in range(n):
            equation = ""
            for j in range(n):
                coeff = matrix[i, j]
                if j == 0:
                    equation += f"{coeff:8.2f}*x{j+1}"
                else:
                    sign = "+" if coeff >= 0 else "-"
                    equation += f" {sign} {abs(coeff):7.2f}*x{j+1}"
            equation += f" = {vector[i]:8.2f}"
            self.results_text.insert(tk.END, equation + "\n")
        
        self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.results_text.insert(tk.END, "PROCESO DE ELIMINACIÓN DE GAUSS:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # Mostrar proceso paso a paso
        steps = self.gauss_solver.get_steps()
        for i, (step_matrix, operation) in enumerate(steps):
            self.results_text.insert(tk.END, f"Paso {i+1}: {operation}\n")
            self.results_text.insert(tk.END, self.gauss_solver.format_matrix(step_matrix) + "\n\n")
        
        # Mostrar solución
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "SOLUCIÓN DEL SISTEMA:\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        
        for i, val in enumerate(solution):
            self.results_text.insert(tk.END, f"x{i+1} = {val:.2f}\n")
        
        # Verificación
        self.results_text.insert(tk.END, "\n" + "=" * 30 + "\n")
        self.results_text.insert(tk.END, "VERIFICACIÓN:\n")
        self.results_text.insert(tk.END, "=" * 30 + "\n")
        
        verification = np.dot(matrix, solution)
        for i in range(n):
            self.results_text.insert(tk.END, 
                f"Ecuación {i+1}: {verification[i]:.2f} ≈ {vector[i]:.2f} "
                f"(Error: {abs(verification[i] - vector[i]):.6f})\n")
        
        messagebox.showinfo("Éxito", "Sistema resuelto correctamente. Consulte el área de resultados para ver el proceso completo.")
    
    def clear_results(self):
        """Limpia el área de resultados."""
        self.results_text.delete('1.0', tk.END)
    
    def load_example(self):
        """Carga un ejemplo de sistema de ecuaciones."""
        # Ejemplo: 3x + 2y - z = 1, 2x - 2y + 4z = 0, -x + 0.5y - z = 0
        self.num_equations.set("3")
        self.update_matrix_size()
        
        # Coeficientes del ejemplo
        example_matrix = [[3, 2, -1], [2, -2, 4], [-1, 0.5, -1]]
        example_vector = [1, 0, 0]
        
        # Rellenar los campos
        for i in range(3):
            for j in range(3):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, str(example_matrix[i][j]))
            
            self.vector_entries[i].delete(0, tk.END)
            self.vector_entries[i].insert(0, str(example_vector[i]))
        
        messagebox.showinfo("Ejemplo Cargado", "Se ha cargado un ejemplo de sistema 3x3.\nPuede resolver el sistema presionando 'Resolver Sistema'.")

def main():
    """Función principal para ejecutar la aplicación."""
    root = tk.Tk()
    
    # Configurar estilos personalizados
    style = ttk.Style()
    style.configure("Invalid.TEntry", fieldbackground="lightcoral")
    style.configure("Accent.TButton", font=("Arial", 12, "bold"))
    
    app = AlgebraCalculator(root)
    
    # Centrar ventana
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
