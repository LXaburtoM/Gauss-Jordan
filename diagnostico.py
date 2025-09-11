#!/usr/bin/env python3


import sys
import os
import platform

def diagnóstico_completo():
    """Ejecuta un diagnóstico completo del sistema."""
    print("=" * 70)
    print("DIAGNÓSTICO COMPLETO - CALCULADORA DE ÁLGEBRA")
    print("=" * 70)
    
    # 1. Información del sistema
    print("\n1. INFORMACIÓN DEL SISTEMA:")
    print(f"   - Sistema operativo: {platform.system()} {platform.release()}")
    print(f"   - Versión de Python: {sys.version}")
    print(f"   - Arquitectura: {platform.architecture()[0]}")
    print(f"   - Directorio actual: {os.getcwd()}")
    
    # 2. Verificar archivos necesarios
    print("\n2. VERIFICACIÓN DE ARCHIVOS:")
    archivos_necesarios = [
        'main.py',
        'calculator_gui.py', 
        'calculator_gui_mejorado.py',
        'modern_calculator_gui.py',
        'gauss_elimination.py',
        'gauss_elimination_mejorado.py',
        'requirements.txt',
        'README.md'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            size = os.path.getsize(archivo)
            print(f"   ✓ {archivo} ({size} bytes)")
        else:
            print(f"   ✗ {archivo} - FALTANTE")
            archivos_faltantes.append(archivo)
    
    # 3. Verificar dependencias
    print("\n3. VERIFICACIÓN DE DEPENDENCIAS:")
    
    # NumPy
    try:
        import numpy as np
        print(f"   ✓ NumPy {np.__version__} instalado correctamente")
    except ImportError as e:
        print(f"   ✗ NumPy no disponible: {e}")
    
    # Tkinter
    try:
        import tkinter as tk
        print(f"   ✓ Tkinter disponible")
        
        # Probar creación de ventana
        try:
            root = tk.Tk()
            root.withdraw()  # No mostrar
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            print(f"   ✓ Tkinter funcional - Pantalla: {width}x{height}")
            root.destroy()
        except Exception as e:
            print(f"   ⚠ Tkinter disponible pero con problemas: {e}")
            
    except ImportError as e:
        print(f"   ✗ Tkinter no disponible: {e}")
    
    # 4. Verificar importaciones de módulos locales
    print("\n4. VERIFICACIÓN DE MÓDULOS LOCALES:")
    
    modulos = [
        ('gauss_elimination', 'GaussElimination'),
        ('gauss_elimination_mejorado', 'GaussEliminationMejorado'),
        ('calculator_gui', 'AlgebraCalculator'),
        ('calculator_gui_mejorado', 'CalculadoraAlgebraGUI'),
        ('modern_calculator_gui', 'ModernAlgebraCalculator')
    ]
    
    for modulo, clase in modulos:
        try:
            mod = __import__(modulo)
            cls = getattr(mod, clase)
            print(f"   ✓ {modulo}.{clase} importado correctamente")
        except ImportError as e:
            print(f"   ✗ Error importando {modulo}: {e}")
        except AttributeError as e:
            print(f"   ⚠ {modulo} importado, pero {clase} no encontrada: {e}")
        except Exception as e:
            print(f"   ✗ Error inesperado con {modulo}: {e}")
    
    # 5. Prueba básica de funcionalidad
    print("\n5. PRUEBA BÁSICA DE FUNCIONALIDAD:")
    
    try:
        import numpy as np
        from gauss_elimination import GaussElimination
        
        # Sistema simple: 2x + y = 5, x - y = 1
        matrix = np.array([[2, 1], [1, -1]], dtype=float)
        vector = np.array([5, 1], dtype=float)
        
        solver = GaussElimination()
        solution, has_solution, error = solver.solve(matrix, vector)
        
        if has_solution:
            print(f"   ✓ Algoritmo básico funcional - Solución: x={solution[0]:.2f}, y={solution[1]:.2f}")
        else:
            print(f"   ⚠ Problema con algoritmo básico: {error}")
            
    except Exception as e:
        print(f"   ✗ Error en prueba básica: {e}")
    
    # 6. Codificación y caracteres especiales
    print("\n6. VERIFICACIÓN DE CODIFICACIÓN:")
    print(f"   - Codificación por defecto: {sys.getdefaultencoding()}")
    print(f"   - Codificación del sistema: {sys.getfilesystemencoding()}")
    
    try:
        test_chars = "áéíóú ñÑ ×²³ 🚀💎📟❌"
        print(f"   ✓ Caracteres especiales soportados: {test_chars}")
    except UnicodeEncodeError:
        print("   ⚠ Problemas con caracteres especiales detectados")
    
    # 7. Resumen y recomendaciones
    print("\n7. RESUMEN Y RECOMENDACIONES:")
    
    if archivos_faltantes:
        print("   ⚠ ARCHIVOS FALTANTES:")
        for archivo in archivos_faltantes:
            print(f"     - {archivo}")
        print("   → Asegúrese de que todos los archivos estén presentes")
    else:
        print("   ✓ Todos los archivos necesarios están presentes")
    
    print("\n   PASOS PARA RESOLVER PROBLEMAS COMUNES:")
    print("   1. Si falta NumPy: pip install numpy")
    print("   2. Si hay problemas con Tkinter en Linux: sudo apt-get install python3-tk")
    print("   3. Si hay problemas de encoding: use main_simple.py en lugar de main.py")
    print("   4. Si persisten problemas, ejecute directamente:")
    print("      - python calculator_gui.py (interfaz básica)")
    print("      - python calculator_gui_mejorado.py (con matrices rectangulares)")
    print("      - python modern_calculator_gui.py (interfaz moderna)")
    
    print("\n" + "=" * 70)
    print("DIAGNÓSTICO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    diagnóstico_completo()
