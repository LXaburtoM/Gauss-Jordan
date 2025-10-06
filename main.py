

import sys
import os

def check_requirements():
    """Verifica que todas las dependencias estén instaladas."""
    try:
        import numpy as np
        print(f"NumPy {np.__version__} encontrado")
    except ImportError:
        print("Error: NumPy no esta instalado.")
        print("Instale con: pip install numpy")
        return False
    
    try:
        import tkinter as tk
        print("Tkinter encontrado")
    except ImportError:
        print("Error: Tkinter no esta disponible.")
        print("En algunas distribuciones de Linux, instale con:")
        print("sudo apt-get install python3-tk")
        return False
    
    return True

def main():
    """Función principal del programa."""
    print("=" * 60)
    print("CALCULADORA DE ÁLGEBRA - ELIMINACIÓN DE GAUSS")
    print("=" * 60)
    print("Verificando dependencias...")
    
    if not check_requirements():
        print("\nNo se pueden satisfacer todas las dependencias.")
        print("Por favor, instale los paquetes requeridos antes de continuar.")
        sys.exit(1)
    
    print("\n✓ Todas las dependencias están disponibles")
    print("Iniciando aplicación...")
    
    # Importar y ejecutar la aplicación
    try:
        # Preguntar qué versión usar
        import tkinter as tk
        from tkinter import messagebox
        
        # Crear ventana principal visible
        root = tk.Tk()
        root.title("Calculadora de Álgebra - Selección")
        root.geometry("550x450")
        root.resizable(False, False)
        root.configure(bg='#f0f0f0')
        
        # Centrar ventana en la pantalla
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Variable para almacenar la elección
        choice = {'value': None}
        
        
        
        def select_choice(val):
            choice['value'] = val
            root.quit()  # Cambiar destroy por quit para salir del mainloop
        
        # Contenido
        tk.Label(root, text="Seleccione la aplicación:", 
                font=('Arial', 16, 'bold'), bg='#f0f0f0').pack(pady=30)
        
        # Descripción
        tk.Label(root, text="Elija entre resolver sistemas de ecuaciones\no realizar operaciones matriciales", 
                font=('Arial', 10), bg='#f0f0f0', fg='#666').pack(pady=10)
        
        tk.Button(root, text="🚀 SISTEMA UNIFICADO\n(Navegar entre interfaces sin cerrar)", 
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 command=lambda: select_choice('unificado'), height=3).pack(pady=15, padx=30, fill='x')
        
        tk.Button(root, text="🧮 CALCULADORA MEJORADA v2.0\n(Solo Sistemas de Ecuaciones)", 
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('mejorada'), height=2).pack(pady=10, padx=30, fill='x')
        
        tk.Button(root, text="🔢 OPERACIONES MATRICIALES\n(Solo Suma y Multiplicación)", 
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('operaciones'), height=2).pack(pady=10, padx=30, fill='x')
        
        tk.Button(root, text="❌ Salir", 
                 bg='#7f8c8d', fg='white', font=('Arial', 11),
                 command=lambda: select_choice(None)).pack(pady=20)
        
        # Manejar cierre de ventana
        def on_closing():
            choice['value'] = None
            root.quit()
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Ejecutar ventana de selección
        root.mainloop()
        
        # Obtener la elección
        selected_choice = choice['value']
        
        # Destruir ventana de selección
        root.destroy()
        
        if selected_choice is None:  # Cancelar
            print("Operacion cancelada por el usuario.")
            return
        elif selected_choice == 'unificado':  # Sistema unificado
            print("Iniciando Sistema Unificado...")
            try:
                from sistema_unificado import main as run_unificado
            except ImportError:
                print("Error: No se encontro el archivo 'sistema_unificado.py'.")
                print("Asegurate de que el archivo este en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_unificado()
        elif selected_choice == 'mejorada':  # Calculadora mejorada
            print("Iniciando Calculadora Mejorada v2.0...")
            try:
                from calculadora_mejorada import main as run_mejorada
            except ImportError:
                print("Error: No se encontro el archivo 'calculadora_mejorada.py'.")
                print("Asegurate de que el archivo este en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_mejorada()
        elif selected_choice == 'operaciones':  # Operaciones matriciales
            print("Iniciando Operaciones Matriciales...")
            try:
                from operaciones_matriciales import main as run_operaciones
            except ImportError:
                print("Error: No se encontro el archivo 'operaciones_matriciales.py'.")
                print("Asegurate de que el archivo este en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_operaciones()
    except ImportError as e:
        print(f"\n✗ Error al importar módulos: {e}")
        print("Asegúrese de que todos los archivos estén en el directorio correcto:")
        print("- main.py")
        print("- calculator_gui.py") 
        print("- calculator_gui_mejorado.py")
        print("- gauss_elimination.py")
        print("- gauss_elimination_mejorado.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()



























