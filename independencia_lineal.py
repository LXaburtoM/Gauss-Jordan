#!/usr/bin/env python3
"""
Módulo de Independencia Lineal
Analiza si un conjunto de vectores es linealmente independiente o dependiente
"""

import numpy as np
from typing import Tuple, List, Dict, Any
from gauss_jordan import GaussJordan

class IndependenciaLineal:
    """
    Clase para analizar la independencia lineal de vectores.
    """
    
    def __init__(self):
        self.pasos = []
        self.operaciones = []
        self.vectores = None
        self.matriz_analisis = None
        self.resultado_analisis = {}
        
    def analizar_vectores(self, vectores: np.ndarray) -> Dict[str, Any]:
        """
        Analiza si un conjunto de vectores es linealmente independiente.
        
        Args:
            vectores: Matriz donde cada columna es un vector (n×m donde m es el número de vectores)
            
        Returns:
            Diccionario con el análisis completo
        """
        self.pasos = []
        self.operaciones = []
        self.vectores = vectores.copy()
        
        n, m = vectores.shape  # n dimensiones, m vectores
        
        resultado = {
            'vectores_originales': vectores.copy(),
            'num_vectores': m,
            'dimension_vectores': n,
            'es_independiente': False,
            'rango': 0,
            'determinante': None,
            'tipo_analisis': '',
            'conclusion': '',
            'explicacion_detallada': [],
            'pasos_reduccion': [],
            'vectores_combinacion_lineal': []
        }
        
        # Determinar tipo de análisis
        if m > n:
            resultado['tipo_analisis'] = 'MAS_VECTORES_QUE_DIMENSIONES'
            resultado['es_independiente'] = False
            resultado['conclusion'] = f'Linealmente DEPENDIENTES: {m} vectores en espacio {n}-dimensional'
            resultado['explicacion_detallada'].append(
                f'Un conjunto de {m} vectores en un espacio {n}-dimensional '
                f'es automáticamente linealmente dependiente cuando m > n.'
            )
        elif m == n:
            resultado['tipo_analisis'] = 'CUADRADO_DETERMINANTE'
            resultado = self._analizar_con_determinante(vectores, resultado)
        else:  # m < n
            resultado['tipo_analisis'] = 'REDUCCION_FILAS'
            resultado = self._analizar_con_reduccion(vectores, resultado)
        
        # Calcular rango siempre
        resultado['rango'] = self._calcular_rango(vectores)
        
        # Conclusión final
        if resultado['es_independiente']:
            resultado['conclusion'] = f'Los {m} vectores son LINEALMENTE INDEPENDIENTES'
        else:
            if resultado['tipo_analisis'] != 'MAS_VECTORES_QUE_DIMENSIONES':
                resultado['conclusion'] = f'Los {m} vectores son LINEALMENTE DEPENDIENTES'
        
        self.resultado_analisis = resultado
        return resultado
    
    def _analizar_con_determinante(self, vectores: np.ndarray, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza independencia usando determinante (matriz cuadrada)."""
        
        det = np.linalg.det(vectores)
        resultado['determinante'] = det
        
        if abs(det) > 1e-10:
            resultado['es_independiente'] = True
            resultado['explicacion_detallada'].append(
                f'Determinante = {det:.6f} ≠ 0, por lo tanto los vectores son linealmente independientes.'
            )
        else:
            resultado['es_independiente'] = False
            resultado['explicacion_detallada'].append(
                f'Determinante = {det:.6f} ≈ 0, por lo tanto los vectores son linealmente dependientes.'
            )
        
        return resultado
    
    def _analizar_con_reduccion(self, vectores: np.ndarray, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Analiza independencia usando reducción por filas."""
        
        # Usar Gauss-Jordan para reducir
        solver = GaussJordan()
        solucion, es_unica, mensaje = solver.resolver(vectores, np.zeros(vectores.shape[0]))
        
        # Obtener información detallada
        info_detallada = solver.obtener_informacion_detallada()
        
        # Guardar pasos
        if hasattr(solver, 'pasos') and solver.pasos:
            self.pasos = solver.pasos
        
        resultado['pasos_reduccion'] = self.pasos
        resultado['rango'] = info_detallada['rango_matriz']
        
        # Determinar independencia
        if resultado['rango'] == vectores.shape[1]:
            resultado['es_independiente'] = True
            resultado['explicacion_detallada'].append(
                f'El rango de la matriz ({resultado["rango"]}) es igual al número de vectores '
                f'({vectores.shape[1]}), por lo tanto son linealmente independientes.'
            )
        else:
            resultado['es_independiente'] = False
            resultado['explicacion_detallada'].append(
                f'El rango de la matriz ({resultado["rango"]}) es menor que el número de vectores '
                f'({vectores.shape[1]}), por lo tanto son linealmente dependientes.'
            )
            
            # Identificar qué vectores son combinación lineal de otros
            if info_detallada.get('variables_libres'):
                resultado['vectores_combinacion_lineal'] = list(info_detallada['variables_libres'])
        
        return resultado
    
    def _calcular_rango(self, matriz: np.ndarray) -> int:
        """Calcula el rango de la matriz."""
        try:
            return np.linalg.matrix_rank(matriz)
        except:
            return 0
    
    def obtener_reporte_completo(self) -> str:
        """Genera un reporte completo del análisis de independencia lineal."""
        if not self.resultado_analisis:
            return "No se ha realizado ningún análisis."
        
        resultado = self.resultado_analisis
        reporte = []
        
        reporte.append("═" * 70)
        reporte.append("ANÁLISIS DE INDEPENDENCIA LINEAL DE VECTORES")
        reporte.append("═" * 70)
        reporte.append("")
        
        # Información básica
        reporte.append("INFORMACIÓN BÁSICA:")
        reporte.append("─" * 30)
        reporte.append(f"• Número de vectores: {resultado['num_vectores']}")
        reporte.append(f"• Dimensión del espacio: {resultado['dimension_vectores']}")
        reporte.append(f"• Rango de la matriz: {resultado['rango']}")
        reporte.append("")
        
        # Vectores originales
        reporte.append("VECTORES ORIGINALES:")
        reporte.append("─" * 30)
        vectores = resultado['vectores_originales']
        for i in range(vectores.shape[1]):
            vector_str = " ".join([f"{vectores[j, i]:8.2f}" for j in range(vectores.shape[0])])
            reporte.append(f"v{i+1} = [{vector_str}]ᵀ")
        reporte.append("")
        
        # Método de análisis
        reporte.append("MÉTODO DE ANÁLISIS:")
        reporte.append("─" * 30)
        if resultado['tipo_analisis'] == 'MAS_VECTORES_QUE_DIMENSIONES':
            reporte.append("• Regla básica: más vectores que dimensiones → dependientes")
        elif resultado['tipo_analisis'] == 'CUADRADO_DETERMINANTE':
            reporte.append("• Cálculo del determinante (matriz cuadrada)")
            reporte.append(f"• Determinante = {resultado['determinante']:.6f}")
        else:
            reporte.append("• Reducción por filas de Gauss-Jordan")
            reporte.append("• Análisis del rango de la matriz")
        reporte.append("")
        
        # Explicación detallada
        reporte.append("ANÁLISIS DETALLADO:")
        reporte.append("─" * 30)
        for explicacion in resultado['explicacion_detallada']:
            reporte.append(f"• {explicacion}")
        reporte.append("")
        
        # Conclusión
        reporte.append("CONCLUSIÓN:")
        reporte.append("─" * 30)
        if resultado['es_independiente']:
            reporte.append("✅ Los vectores son LINEALMENTE INDEPENDIENTES")
            reporte.append("   → Ningún vector puede expresarse como combinación lineal de los otros")
            reporte.append("   → El conjunto forma una base del subespacio generado")
        else:
            reporte.append("❌ Los vectores son LINEALMENTE DEPENDIENTES")
            reporte.append("   → Existe al menos un vector que es combinación lineal de los otros")
            reporte.append("   → El conjunto NO forma una base")
            
            if resultado['vectores_combinacion_lineal']:
                vectores_dep = [f"v{i}" for i in resultado['vectores_combinacion_lineal']]
                reporte.append(f"   → Vector(es) dependiente(s): {', '.join(vectores_dep)}")
        
        reporte.append("")
        reporte.append("═" * 70)
        
        return "\n".join(reporte)

# Función auxiliar para las interfaces
def analizar_independencia_vectores(vectores: np.ndarray) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Función simplificada para usar en las interfaces.
    
    Returns:
        Tuple con (es_independiente, conclusion_texto, info_completa)
    """
    analizador = IndependenciaLineal()
    resultado = analizador.analizar_vectores(vectores)
    
    reporte = analizador.obtener_reporte_completo()
    
    return resultado['es_independiente'], resultado['conclusion'], {
        'reporte_completo': reporte,
        'info_detallada': resultado
    }
