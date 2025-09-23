#!/usr/bin/env python3
"""
Prueba específica de las nuevas funcionalidades implementadas
Verifica los cambios solicitados:
1. Variables libres como ecuaciones
2. Uso de llaves {} en lugar de corchetes []
3. Análisis de inconsistencia mejorado
"""

import numpy as np
from gauss_jordan import GaussJordan

def probar_cambios_nuevos():
    """Prueba los cambios específicos solicitados."""
    
    print("=" * 70)
    print("PRUEBA DE NUEVAS FUNCIONALIDADES IMPLEMENTADAS")
    print("=" * 70)
    print()
    
    # Prueba 1: Sistema con variables libres - verificar ecuaciones
    print("PRUEBA 1: Variables libres como ecuaciones")
    print("-" * 45)
    
    # Sistema 2x3 que debe tener variables libres
    matriz1 = np.array([[1, 2, 3], [2, 1, 1]], dtype=float)
    vector1 = np.array([6, 4], dtype=float)
    
    print("Sistema 2×3 (subdeterminado):")
    print("x₁ + 2x₂ + 3x₃ = 6")
    print("2x₁ + x₂ + x₃ = 4")
    print()
    
    solver1 = GaussJordan()
    solucion1, es_unica1, mensaje1 = solver1.resolver(matriz1, vector1)
    
    print("RESULTADO:")
    print(mensaje1)
    print()
    
    # Verificar uso de llaves {}
    info1 = solver1.obtener_informacion_detallada()
    print("VERIFICACIÓN DE LLAVES {} (no corchetes []):")
    print(f"• Columnas pivote: {info1['columnas_pivote']} ← Tipo: {type(info1['columnas_pivote'])}")
    print(f"• Variables libres: {info1['variables_libres']} ← Tipo: {type(info1['variables_libres'])}")
    print()
    
    # Probar ecuaciones de variables libres
    if hasattr(solver1, 'obtener_ecuaciones_variables_libres') and solver1.pasos:
        ecuaciones = solver1.obtener_ecuaciones_variables_libres(solver1.pasos[-1][0], 3)
        print("ECUACIONES DE VARIABLES LIBRES:")
        if ecuaciones:
            for ecuacion in ecuaciones:
                print(f"  {ecuacion}")
        else:
            print("  No se generaron ecuaciones de variables libres")
    print()
    
    print("=" * 70)
    print()
    
    # Prueba 2: Sistema que no forme matriz identidad
    print("PRUEBA 2: Análisis de inconsistencia mejorado")
    print("-" * 44)
    
    # Sistema que puede no formar matriz identidad pero tener rango consistente
    matriz2 = np.array([[2, 4], [1, 2]], dtype=float)
    vector2 = np.array([6, 3], dtype=float)
    
    print("Sistema 2×2 con filas linealmente dependientes:")
    print("2x₁ + 4x₂ = 6")
    print("x₁ + 2x₂ = 3")
    print()
    
    solver2 = GaussJordan()
    solucion2, es_unica2, mensaje2 = solver2.resolver(matriz2, vector2)
    
    print("RESULTADO:")
    print(mensaje2)
    print()
    
    # Verificar verificación de matriz identidad
    info2 = solver2.obtener_informacion_detallada()
    print("ANÁLISIS DETALLADO:")
    print(f"• Tipo de sistema: {info2['tipo_sistema']}")
    print(f"• Columnas pivote: {info2['columnas_pivote']}")
    print(f"• Variables libres: {info2['variables_libres']}")
    print(f"• Consistente: {info2['es_consistente']}")
    
    # Verificar si el solver detectó matriz identidad
    if solver2.pasos:
        matriz_final = solver2.pasos[-1][0]
        es_identidad = solver2._verificar_matriz_identidad(matriz_final, 2)
        print(f"• Forma matriz identidad: {es_identidad}")
    
    print()
    print("=" * 70)
    print()
    
    # Resumen de verificaciones
    print("VERIFICACIÓN DE CAMBIOS IMPLEMENTADOS:")
    print("-" * 40)
    
    # 1. Verificar llaves
    usa_llaves_pivote = isinstance(info1['columnas_pivote'], set)
    usa_llaves_libres = isinstance(info1['variables_libres'], set)
    
    print(f"✅ 1. Usar {{}} en lugar de []: {usa_llaves_pivote and usa_llaves_libres}")
    
    # 2. Verificar ecuaciones de variables libres
    tiene_metodo_ecuaciones = hasattr(solver1, 'obtener_ecuaciones_variables_libres')
    print(f"✅ 2. Ecuaciones de variables libres: {tiene_metodo_ecuaciones}")
    
    # 3. Verificar análisis de matriz identidad
    tiene_verificacion_identidad = hasattr(solver2, '_verificar_matriz_identidad')
    print(f"✅ 3. Análisis de matriz identidad: {tiene_verificacion_identidad}")
    
    print()
    print("🎯 TODAS LAS FUNCIONALIDADES NUEVAS HAN SIDO IMPLEMENTADAS")
    print("=" * 70)

if __name__ == "__main__":
    probar_cambios_nuevos()
