import numpy as np
from typing import Tuple, List, Optional, Dict, Set

class GaussJordan:
    """
    Clase para resolver sistemas de ecuaciones lineales usando eliminacion de Gauss-Jordan.
    Soporta matrices rectangulares y detecta columnas pivotes, variables libres,
    y clasifica sistemas como unicos, infinitos o inconsistentes.
    """
    
    def __init__(self):
        self.pasos = []  # Almacena los pasos de la eliminacion
        self.operaciones = []  # Almacena las operaciones realizadas
        self.columnas_pivote = []  # Indices de columnas pivote
        self.variables_libres = []  # Indices de variables libres
        self.rango_matriz = 0  # Rango de la matriz de coeficientes
        self.rango_aumentada = 0  # Rango de la matriz aumentada
        self.tipo_sistema = ""  # Tipo de sistema: unico, infinito, inconsistente
    
    def resolver(self, matriz: np.ndarray, vector: np.ndarray) -> Tuple[Optional[np.ndarray], bool, str]:
        """
        Resuelve el sistema de ecuaciones Ax = b usando eliminacion de Gauss-Jordan.
        
        Args:
            matriz: Matriz de coeficientes A (m x n)
            vector: Vector independiente b (m x 1)
            
        Returns:
            Tuple con:
            - Solucion del sistema (None si no existe solucion)
            - Boolean indicando si tiene solucion unica
            - Mensaje con informacion del sistema
        """
        try:
            # Reiniciar todos los datos
            self._reiniciar_datos()
            
            # Validar dimensiones
            m, n = matriz.shape  # m = ecuaciones, n = variables
            if len(vector) != m:
                return None, False, f"Dimensiones incompatibles: matriz {m}x{n}, vector {len(vector)}x1"
            
            # Crear matriz aumentada
            aumentada = np.column_stack((matriz.astype(float), vector.astype(float)))
            
            # Guardar estado inicial
            self.pasos.append(aumentada.copy())
            self.operaciones.append(f"Matriz aumentada inicial ({m}x{n+1})")
            
            # FASE 1: Reduccion a forma escalonada reducida
            fila_actual = 0
            for col in range(n):  # Procesar cada columna
                # Buscar pivote en la columna actual
                fila_pivote = self._buscar_pivote(aumentada, fila_actual, col, m)
                
                if fila_pivote == -1:
                    # No hay pivote en esta columna (variable libre)
                    self.variables_libres.append(col)
                    continue
                
                # Intercambiar filas si es necesario
                if fila_pivote != fila_actual:
                    aumentada[[fila_actual, fila_pivote]] = aumentada[[fila_pivote, fila_actual]]
                    self.pasos.append(aumentada.copy())
                    self.operaciones.append(f"Intercambiar fila {fila_actual+1} con fila {fila_pivote+1}")
                
                # Registrar columna pivote
                self.columnas_pivote.append(col)
                
                # Hacer el pivote igual a 1
                pivote = aumentada[fila_actual, col]
                if abs(pivote - 1.0) > 1e-10:
                    aumentada[fila_actual] = aumentada[fila_actual] / pivote
                    self.pasos.append(aumentada.copy())
                    self.operaciones.append(f"F{fila_actual+1} = F{fila_actual+1} / {pivote:.2f}")
                
                # Eliminar todos los otros elementos en esta columna
                for i in range(m):
                    if i != fila_actual and abs(aumentada[i, col]) > 1e-10:
                        factor = aumentada[i, col]
                        aumentada[i] = aumentada[i] - factor * aumentada[fila_actual]
                        self.pasos.append(aumentada.copy())
                        self.operaciones.append(f"F{i+1} = F{i+1} - ({factor:.2f}) * F{fila_actual+1}")
                
                fila_actual += 1
                if fila_actual >= m:
                    break
            
            # FASE 2: Analizar el sistema
            return self._analizar_sistema(aumentada, m, n)
            
        except Exception as e:
            return None, False, f"Error en el calculo: {str(e)}"
    
    def _reiniciar_datos(self):
        """Reinicia todas las variables de analisis."""
        self.pasos = []
        self.operaciones = []
        self.columnas_pivote = []
        self.variables_libres = []
        self.rango_matriz = 0
        self.rango_aumentada = 0
        self.tipo_sistema = ""
    
    def _buscar_pivote(self, matriz: np.ndarray, fila_inicio: int, col: int, m: int) -> int:
        """
        Busca la fila con el mayor elemento en valor absoluto para usar como pivote.
        
        Args:
            matriz: Matriz aumentada
            fila_inicio: Fila donde empezar a buscar
            col: Columna donde buscar el pivote
            m: Numero de filas
            
        Returns:
            Indice de la fila con el mayor pivote, -1 si todos son cero
        """
        max_val = 0
        fila_pivote = -1
        
        for i in range(fila_inicio, m):
            if abs(matriz[i, col]) > max_val:
                max_val = abs(matriz[i, col])
                fila_pivote = i
        
        return fila_pivote if max_val > 1e-10 else -1
    
    def _analizar_sistema(self, aumentada: np.ndarray, m: int, n: int) -> Tuple[Optional[np.ndarray], bool, str]:
        """
        Analiza el sistema resuelto y clasifica el tipo de solucion.
        
        Args:
            aumentada: Matriz aumentada en forma escalonada reducida
            m: Numero de ecuaciones
            n: Numero de variables
            
        Returns:
            Tupla con solucion, es_unica, mensaje_informativo
        """
        # Calcular rangos
        self.rango_matriz = len(self.columnas_pivote)
        self.rango_aumentada = self._calcular_rango_aumentada(aumentada, m, n)
        
        # Completar lista de variables libres
        for i in range(n):
            if i not in self.columnas_pivote:
                if i not in self.variables_libres:
                    self.variables_libres.append(i)
        
        # Verificar consistencia
        if self.rango_aumentada > self.rango_matriz:
            self.tipo_sistema = "inconsistente"
            mensaje = f"Sistema inconsistente (sin solucion)\n"
            mensaje += f"Rango matriz: {self.rango_matriz}, Rango aumentada: {self.rango_aumentada}\n"
            mensaje += f"Columnas pivote: {[c+1 for c in self.columnas_pivote]}"
            return None, False, mensaje
        
        # Sistema consistente
        if self.rango_matriz == n:
            # Solucion unica
            self.tipo_sistema = "unico"
            solucion = self._extraer_solucion_unica(aumentada, n)
            mensaje = f"Sistema con solucion unica\n"
            mensaje += f"Rango: {self.rango_matriz}\n"
            mensaje += f"Columnas pivote: {[c+1 for c in self.columnas_pivote]}\n"
            mensaje += f"Variables libres: Ninguna"
            return solucion, True, mensaje
        else:
            # Infinitas soluciones
            self.tipo_sistema = "infinito"
            solucion = self._extraer_solucion_particular(aumentada, n)
            num_libres = len(self.variables_libres)
            mensaje = f"Sistema con infinitas soluciones\n"
            mensaje += f"Rango: {self.rango_matriz}\n"
            mensaje += f"Columnas pivote: {[c+1 for c in self.columnas_pivote]}\n"
            mensaje += f"Variables libres: {[v+1 for v in self.variables_libres]} ({num_libres} variables)"
            return solucion, False, mensaje
    
    def _calcular_rango_aumentada(self, aumentada: np.ndarray, m: int, n: int) -> int:
        """Calcula el rango de la matriz aumentada."""
        rango = len(self.columnas_pivote)
        
        # Verificar si hay filas no nulas adicionales
        for i in range(len(self.columnas_pivote), m):
            if abs(aumentada[i, n]) > 1e-10:  # Elemento no nulo en columna aumentada
                rango += 1
                break
        
        return rango
    
    def _extraer_solucion_unica(self, aumentada: np.ndarray, n: int) -> np.ndarray:
        """Extrae la solucion cuando el sistema tiene solucion unica."""
        solucion = np.zeros(n)
        for i, col in enumerate(self.columnas_pivote):
            solucion[col] = aumentada[i, n]
        return solucion
    
    def _extraer_solucion_particular(self, aumentada: np.ndarray, n: int) -> np.ndarray:
        """Extrae una solucion particular (variables libres = 0)."""
        solucion = np.zeros(n)
        for i, col in enumerate(self.columnas_pivote):
            solucion[col] = aumentada[i, n]
        return solucion
    
    def obtener_pasos(self) -> List[Tuple[np.ndarray, str]]:
        """
        Retorna los pasos del proceso de eliminacion.
        
        Returns:
            Lista de tuplas (matriz, operacion)
        """
        return list(zip(self.pasos, self.operaciones))
    
    def formatear_matriz(self, matriz: np.ndarray, decimales: int = 2) -> str:
        """
        Formatea una matriz para mostrarla de manera legible.
        
        Args:
            matriz: Matriz a formatear
            decimales: Numero de decimales a mostrar
            
        Returns:
            String con la matriz formateada
        """
        filas = []
        for fila in matriz:
            fila_formateada = []
            for val in fila[:-1]:  # Coeficientes
                fila_formateada.append(f"{val:8.{decimales}f}")
            fila_formateada.append("  |")
            fila_formateada.append(f"{fila[-1]:8.{decimales}f}")  # Termino independiente
            filas.append(" ".join(fila_formateada))
        
        return "\n".join(filas)
    
    def obtener_informacion_detallada(self) -> Dict[str, any]:
        """
        Retorna informacion detallada del analisis del sistema.
        
        Returns:
            Diccionario con toda la informacion del sistema
        """
        return {
            'tipo_sistema': self.tipo_sistema,
            'rango_matriz': self.rango_matriz,
            'rango_aumentada': self.rango_aumentada,
            'columnas_pivote': [c + 1 for c in self.columnas_pivote],  # Base 1
            'variables_libres': [v + 1 for v in self.variables_libres],  # Base 1
            'num_variables_libres': len(self.variables_libres),
            'es_consistente': self.rango_matriz == self.rango_aumentada,
            'tiene_solucion_unica': self.tipo_sistema == "unico"
        }
