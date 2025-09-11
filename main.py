

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
        root.title("Selección de Interfaz")
        root.geometry("420x280")
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
        tk.Label(root, text="¿Qué interfaz desea usar?", 
                font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=20)
        
        tk.Button(root, text="🌟 NUEVA: Calculadora Mejorada\n(Sistema Completo Actualizado en Español)", 
                 bg='#e74c3c', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('mejorada'), height=2).pack(pady=5, padx=20, fill='x')
        
        tk.Button(root, text="🎆 Sistema Completo Original\n(Matrices rectangulares + Gauss-Jordan avanzado)", 
                 bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('unificada'), height=2).pack(pady=5, padx=20, fill='x')
        
        tk.Button(root, text="💎 Interfaz Moderna (Clásica)\n(Solo sistemas cuadrados)", 
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('moderna'), height=2).pack(pady=5, padx=20, fill='x')
        
        tk.Button(root, text="📟 Interfaz Clásica\n(Básica)", 
                 bg='#95a5a6', fg='white', font=('Arial', 11, 'bold'),
                 command=lambda: select_choice('clasica'), height=2).pack(pady=5, padx=20, fill='x')
        
        tk.Button(root, text="❌ Salir", 
                 bg='#7f8c8d', fg='white', font=('Arial', 11),
                 command=lambda: select_choice(None)).pack(pady=(10, 5))
        
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
        elif selected_choice == 'mejorada':  # Nueva calculadora mejorada
            print("Iniciando calculadora mejorada...")
            try:
                from calculadora_mejorada import main as run_mejorada
            except ImportError:
                print("Error: No se encontro el archivo 'calculadora_mejorada.py'.")
                print("Asegurate de que el archivo este en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_mejorada()
        elif selected_choice == 'unificada':  # Interfaz unificada original
            print("Iniciando sistema completo unificado...")
            try:
                from calculadora_unificada import main as run_unificada
            except ImportError:
                print("Error: No se encontro el archivo 'calculadora_unificada.py'.")
                print("Asegurate de que el archivo este en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_unificada()
        elif selected_choice == 'moderna':  # Interfaz Moderna
            print("Iniciando interfaz moderna...")
            try:
                from modern_calculator_gui import main as run_modern_calculator
            except ImportError:
                print("✗ Error: No se encontró el archivo 'modern_calculator_gui.py'.")
                print("Asegúrate de que el archivo esté en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_modern_calculator()
        elif selected_choice == 'clasica':  # Interfaz Clásica
            print("Iniciando interfaz clásica...")
            try:
                from calculator_gui import main as run_calculator
            except ImportError:
                print("✗ Error: No se encontró el archivo 'calculator_gui.py'.")
                print("Asegúrate de que el archivo esté en la misma carpeta que 'main.py'.")
                sys.exit(1)
            run_calculator()
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
