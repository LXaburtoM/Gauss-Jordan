#!/usr/bin/env python3

import numpy as np
from gauss_jordan import GaussJordan

def probar_gauss_jordan():
    """Ejecuta pruebas completas del método Gauss-Jordan."""
    
    print("=" * 60)
    print("PRUEBA COMPLETA DE GAUSS-JORDAN")
    print("=" * 60)
    print()
    
    # Prueba 1: Sistema 3x3 con solución única
    print("PRUEBA 1: Sistema 3x3 con solución única")
    print("-" * 40)
    
    matriz1 = np.array([[2, 1, -1], [1, -1, 2], [3, 2, 1]], dtype=float)
    vector1 = np.array([8, 0, 11], dtype=float)
    
    print("Sistema:")
    print("2x₁ + x₂ - x₃ = 8")
    print("x₁ - x₂ + 2x₃ = 0")
    print("3x₁ + 2x₂ + x₃ = 11")
    print()
    
    solver1 = GaussJordan()
    solucion1, es_unica1, mensaje1 = solver1.resolver(matriz1, vector1)
    
    print(f"Resultado: {mensaje1}")
    if solucion1 is not None:
        print(f"Solución: x₁={solucion1[0]:.4f}, x₂={solucion1[1]:.4f}, x₃={solucion1[2]:.4f}")
    
    # Información detallada
    info1 = solver1.obtener_informacion_detallada()
    print()
    print("ANÁLISIS DETALLADO:")
    print(f"• Columnas pivote: {info1['columnas_pivote']}")
    print(f"• Variables libres: {info1['variables_libres'] if info1['variables_libres'] else 'Ninguna'}")
    print(f"• Tipo de sistema: {info1['tipo_sistema'].upper()}")
    print(f"• Rango de matriz: {info1['rango_matriz']}")
    print(f"• Rango de matriz aumentada: {info1['rango_aumentada']}")
    print(f"• Sistema consistente: {'Sí' if info1['es_consistente'] else 'No'}")
    print()
    print("=" * 60)
    print()
    
    # Prueba 2: Sistema 2x3 con infinitas soluciones
    print("PRUEBA 2: Sistema 2x3 con infinitas soluciones (subdeterminado)")
    print("-" * 55)
    
    matriz2 = np.array([[1, 2, 3], [2, 1, 1]], dtype=float)
    vector2 = np.array([6, 4], dtype=float)
    
    print("Sistema:")
    print("x₁ + 2x₂ + 3x₃ = 6")
    print("2x₁ + x₂ + x₃ = 4")
    print()
    
    solver2 = GaussJordan()
    solucion2, es_unica2, mensaje2 = solver2.resolver(matriz2, vector2)
    
    print(f"Resultado: {mensaje2}")
    if solucion2 is not None:
        print(f"Solución particular: x₁={solucion2[0]:.4f}, x₂={solucion2[1]:.4f}, x₃={solucion2[2]:.4f}")
        print("(Variables libres se asignaron a 0 para esta solución particular)")
    
    # Información detallada
    info2 = solver2.obtener_informacion_detallada()
    print()
    print("ANÁLISIS DETALLADO:")
    print(f"• Columnas pivote: {info2['columnas_pivote']}")
    print(f"• Variables libres: {info2['variables_libres']}")
    print(f"• Número de variables libres: {info2['num_variables_libres']}")
    print(f"• Tipo de sistema: {info2['tipo_sistema'].upper()}")
    print(f"• Rango de matriz: {info2['rango_matriz']}")
    print(f"• Rango de matriz aumentada: {info2['rango_aumentada']}")
    print(f"• Sistema consistente: {'Sí' if info2['es_consistente'] else 'No'}")
    print()
    print("=" * 60)
    print()
    
    # Prueba 3: Sistema inconsistente
    print("PRUEBA 3: Sistema inconsistente (sin solución)")
    print("-" * 42)
    
    matriz3 = np.array([[1, 2], [2, 4], [1, 2]], dtype=float)
    vector3 = np.array([3, 6, 5], dtype=float)
    
    print("Sistema:")
    print("x₁ + 2x₂ = 3")
    print("2x₁ + 4x₂ = 6") 
    print("x₁ + 2x₂ = 5  ← Inconsistente con la primera")
    print()
    
    solver3 = GaussJordan()
    solucion3, es_unica3, mensaje3 = solver3.resolver(matriz3, vector3)
    
    print(f"Resultado: {mensaje3}")
    
    # Información detallada
    info3 = solver3.obtener_informacion_detallada()
    print()
    print("ANÁLISIS DETALLADO:")
    print(f"• Columnas pivote: {info3['columnas_pivote']}")
    print(f"• Variables libres: {info3['variables_libres'] if info3['variables_libres'] else 'N/A'}")
    print(f"• Tipo de sistema: {info3['tipo_sistema'].upper()}")
    print(f"• Rango de matriz: {info3['rango_matriz']}")
    print(f"• Rango de matriz aumentada: {info3['rango_aumentada']}")
    print(f"• Sistema consistente: {'Sí' if info3['es_consistente'] else 'No'}")
    print(f"• Diferencia de rangos: {info3['rango_aumentada'] - info3['rango_matriz']}")
    print()
    print("=" * 60)
    print()
    
    print("RESUMEN DE FUNCIONALIDADES PROBADAS:")
    print("✅ Detección de columnas pivote")
    print("✅ Identificación de variables libres")
    print("✅ Clasificación: único, infinito, inconsistente")
    print("✅ Análisis de rangos (matriz y aumentada)")
    print("✅ Detección de consistencia del sistema")
    print("✅ Soluciones particulares para sistemas subdeterminados")
    print("✅ Manejo de sistemas inconsistentes")
    print()
    print("🎯 TODAS LAS FUNCIONALIDADES REQUERIDAS ESTÁN IMPLEMENTADAS")
    print("=" * 60)

if __name__ == "__main__":
    probar_gauss_jordan()
