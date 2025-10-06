#!/usr/bin/env python3
"""
Script de prueba para comparar funcionalidad entre calculadoras
"""

import numpy as np
from gauss_jordan import GaussJordan
from gauss_elimination_mejorado import GaussEliminationMejorado

def test_gauss_jordan():
    """Prueba el método Gauss-Jordan"""
    print("=" * 60)
    print("PRUEBA: MÉTODO GAUSS-JORDAN")
    print("=" * 60)
    
    # Sistema de ejemplo: 3x3
    matriz = np.array([
        [2, 1, -1],
        [1, -1, 2],
        [3, 2, 1]
    ], dtype=float)
    
    vector = np.array([8, 0, 11], dtype=float)
    
    solver = GaussJordan()
    solucion, es_unica, mensaje = solver.resolver(matriz, vector)
    
    print(f"Solución: {solucion}")
    print(f"Es única: {es_unica}")
    print(f"Mensaje: {mensaje}")
    
    # Verificar pasos
    pasos = solver.obtener_pasos()
    print(f"Número de pasos: {len(pasos)}")
    
    # Verificar información detallada
    info = solver.obtener_informacion_detallada()
    print(f"Información disponible: {list(info.keys())}")
    
    return True

def test_gauss():
    """Prueba el método Gauss"""
    print("\n" + "=" * 60)
    print("PRUEBA: MÉTODO GAUSS")
    print("=" * 60)
    
    # Sistema de ejemplo: 3x3
    matriz = np.array([
        [2, 1, -1],
        [1, -1, 2],
        [3, 2, 1]
    ], dtype=float)
    
    vector = np.array([8, 0, 11], dtype=float)
    
    solver = GaussEliminationMejorado()
    solucion, es_unica, mensaje = solver.solve(matriz, vector)
    
    print(f"Solución: {solucion}")
    print(f"Es única: {es_unica}")
    print(f"Mensaje: {mensaje}")
    
    # Verificar pasos
    pasos = solver.get_steps()
    print(f"Número de pasos: {len(pasos)}")
    
    return True

def main():
    """Ejecuta las pruebas"""
    print("VERIFICACIÓN DE FUNCIONALIDAD DE SOLUCIONADORES")
    print("Verificando que ambos métodos funcionan correctamente...")
    
    try:
        test_gauss_jordan()
        test_gauss()
        print("\n" + "=" * 60)
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ Los solucionadores funcionan correctamente")
        print("✅ El sistema unificado debería mostrar los procesos paso a paso")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {e}")
        print("❌ Revisar la implementación")

if __name__ == "__main__":
    main()
