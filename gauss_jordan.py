import numpy as np
from typing import Tuple, List, Optional, Dict, Set

class GaussJordan:
   
    
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
            mensaje += f"Columnas pivote: {{{', '.join(str(c+1) for c in self.columnas_pivote)}}}\n"
            mensaje += f"Variables libres: Ninguna"
            return solucion, True, mensaje
        else:
            # Verificar si realmente forma matriz identidad en las columnas pivote
            es_matriz_identidad = self._verificar_matriz_identidad(aumentada, n)
            
            if es_matriz_identidad:
                # Infinitas soluciones
                self.tipo_sistema = "infinito"
                solucion = self._extraer_solucion_particular(aumentada, n)
                num_libres = len(self.variables_libres)
                mensaje = f"Sistema con infinitas soluciones\n"
                mensaje += f"Rango: {self.rango_matriz}\n"
                mensaje += f"Columnas pivote: {{{', '.join(str(c+1) for c in self.columnas_pivote)}}}\n"
                mensaje += f"Variables libres: {{{', '.join(str(v+1) for v in self.variables_libres)}}} ({num_libres} variables)"
                return solucion, False, mensaje
            else:
                # No forma matriz identidad - inconsistente
                self.tipo_sistema = "inconsistente"
                mensaje = f"Sistema inconsistente\n"
                mensaje += f"Rango: {self.rango_matriz}\n"
                mensaje += f"No forma matriz identidad en las columnas pivote\n"
                mensaje += f"Columnas pivote: {{{', '.join(str(c+1) for c in self.columnas_pivote)}}}"
                return None, False, mensaje
    
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
            'columnas_pivote': {c + 1 for c in self.columnas_pivote},  # Base 1 con llaves
            'variables_libres': {v + 1 for v in self.variables_libres},  # Base 1 con llaves
            'num_variables_libres': len(self.variables_libres),
            'es_consistente': self.rango_matriz == self.rango_aumentada,
            'tiene_solucion_unica': self.tipo_sistema == "unico"
        }
    
    def obtener_ecuaciones_variables_libres(self, aumentada: np.ndarray, n: int) -> List[str]:
        """
        Genera las ecuaciones para las variables libres en terminos de las variables basicas.
        
        Args:
            aumentada: Matriz aumentada en forma escalonada reducida
            n: Numero de variables
            
        Returns:
            Lista de ecuaciones para las variables libres
        """
        ecuaciones = []
        
        if not self.variables_libres or aumentada is None:
            return ecuaciones
        
        # Asegurar que aumentada es una matriz 2D
        if len(aumentada.shape) == 1:
            return ecuaciones
            
        # Para cada variable libre, expresarla en términos de variables básicas
        for var_libre in self.variables_libres:
            # Buscar si esta variable libre aparece en alguna fila
            ecuacion_partes = []
            
            # Examinar cada fila pivote
            for i, col_pivote in enumerate(self.columnas_pivote):
                if i < len(aumentada) and var_libre < aumentada.shape[1] - 1:  # No incluir columna aumentada
                    coef = -aumentada[i, var_libre]  # Negativo porque lo pasamos al otro lado
                    
                    if abs(coef) > 1e-10:  # Si el coeficiente no es cero
                        termino_independiente = aumentada[i, -1]  # Término independiente
                        
                        if coef > 0:
                            if len(ecuacion_partes) == 0:
                                ecuacion_partes.append(f"{coef:.2f}x{col_pivote + 1}")
                            else:
                                ecuacion_partes.append(f" + {coef:.2f}x{col_pivote + 1}")
                        else:
                            ecuacion_partes.append(f" - {abs(coef):.2f}x{col_pivote + 1}")
                        
                        # Agregar término independiente si existe
                        if abs(termino_independiente) > 1e-10:
                            if termino_independiente > 0:
                                ecuacion_partes.append(f" + {termino_independiente:.2f}")
                            else:
                                ecuacion_partes.append(f" - {abs(termino_independiente):.2f}")
                        
                        break  # Solo una ecuación por variable libre
            
            if ecuacion_partes:
                ecuacion = f"x{var_libre + 1} = {''.join(ecuacion_partes)}"
            else:
                ecuacion = f"x{var_libre + 1} = t{var_libre + 1}  (parámetro libre)"
                
            ecuaciones.append(ecuacion)
            
        return ecuaciones
    
    def _verificar_matriz_identidad(self, aumentada: np.ndarray, n: int) -> bool:
        """
        Verifica si las columnas pivote forman una matriz identidad.
        
        Args:
            aumentada: Matriz aumentada en forma escalonada reducida
            n: Numero de variables
            
        Returns:
            True si forma matriz identidad, False en caso contrario
        """
        if aumentada is None or len(aumentada.shape) != 2:
            return False
            
        # Para cada columna pivote, verificar que tenga un 1 en la fila correspondiente
        # y ceros en las demas filas
        for i, col_pivote in enumerate(self.columnas_pivote):
            if i >= aumentada.shape[0] or col_pivote >= aumentada.shape[1] - 1:
                return False
                
            # Verificar que hay un 1 en la posicion [i, col_pivote]
            if abs(aumentada[i, col_pivote] - 1.0) > 1e-10:
                return False
                
            # Verificar que hay ceros en las otras filas de esta columna
            for j in range(aumentada.shape[0]):
                if j != i and abs(aumentada[j, col_pivote]) > 1e-10:
                    return False
                    
        return True
