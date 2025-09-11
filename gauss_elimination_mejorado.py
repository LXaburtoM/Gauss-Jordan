import numpy as np
from typing import Tuple, List, Optional, Union

class GaussEliminationMejorado:
   
    
    def __init__(self):
        self.steps = []  # Almacena los pasos de la eliminación
        self.operations = []  # Almacena las operaciones realizadas
    
    def solve(self, matrix: np.ndarray, vector: np.ndarray) -> Tuple[Optional[np.ndarray], bool, str]:
        """
        Resuelve el sistema de ecuaciones Ax = b usando eliminación de Gauss.
        Soporta matrices rectangulares.
        
        Args:
            matrix: Matriz de coeficientes A (m × n)
            vector: Vector independiente b (m × 1)
            
        Returns:
            Tuple con:
            - Solución del sistema (None si no tiene solución única)
            - Boolean indicando si tiene solución única
            - Mensaje de error/información si aplica
        """
        try:
            # Reiniciar pasos y operaciones
            self.steps = []
            self.operations = []
            
            # Validar dimensiones
            m, n = matrix.shape  # m = número de ecuaciones, n = número de variables
            if len(vector) != m:
                return None, False, f"Dimensiones incompatibles: matriz {m}×{n}, vector {len(vector)}×1"
            
            # Crear matriz aumentada
            augmented = np.column_stack((matrix.astype(float), vector.astype(float)))
            
            # Guardar matriz inicial
            self.steps.append(augmented.copy())
            self.operations.append(f"Matriz aumentada inicial ({m}×{n+1}):")
            
            # Análisis inicial del sistema
            if m > n:
                self.operations.append(f"Sistema sobredeterminado: {m} ecuaciones, {n} incógnitas")
            elif m < n:
                self.operations.append(f"Sistema subdeterminado: {m} ecuaciones, {n} incógnitas")
            else:
                self.operations.append(f"Sistema cuadrado: {m} ecuaciones, {n} incógnitas")
            
            # Eliminación hacia adelante
            rank = 0  # Rango de la matriz
            pivot_cols = []  # Columnas pivote
            
            for col in range(min(m, n)):  # Procesar hasta min(filas, columnas)
                # Buscar pivote en la columna actual
                pivot_row = self._find_pivot_rectangular(augmented, rank, col)
                
                if pivot_row == -1:
                    # No hay pivote en esta columna, continuar con la siguiente
                    continue
                
                # Intercambiar filas si es necesario
                if pivot_row != rank:
                    augmented[[rank, pivot_row]] = augmented[[pivot_row, rank]]
                    self.steps.append(augmented.copy())
                    self.operations.append(f"Intercambiar fila {rank+1} con fila {pivot_row+1}")
                
                # Verificar si el pivote es válido
                if abs(augmented[rank, col]) < 1e-10:
                    continue
                
                pivot_cols.append(col)
                
                # Eliminar elementos debajo del pivote
                for i in range(rank + 1, m):
                    if abs(augmented[i, col]) > 1e-10:
                        factor = augmented[i, col] / augmented[rank, col]
                        augmented[i] = augmented[i] - factor * augmented[rank]
                        
                        self.steps.append(augmented.copy())
                        self.operations.append(f"F{i+1} = F{i+1} - ({factor:.2f}) * F{rank+1}")
                
                rank += 1
            
            # Analizar el resultado
            return self._analyze_solution(augmented, m, n, rank, pivot_cols)
            
        except Exception as e:
            return None, False, f"Error en el cálculo: {str(e)}"
    
    def _find_pivot_rectangular(self, matrix: np.ndarray, start_row: int, col: int) -> int:
        """
        Encuentra el mejor pivote en una columna específica para matrices rectangulares.
        
        Args:
            matrix: Matriz aumentada
            start_row: Fila donde empezar a buscar
            col: Columna donde buscar el pivote
            
        Returns:
            Índice de la fila con el mejor pivote, -1 si no hay pivote válido
        """
        m = matrix.shape[0]
        max_val = 0
        pivot_row = -1
        
        for i in range(start_row, m):
            if abs(matrix[i, col]) > max_val:
                max_val = abs(matrix[i, col])
                pivot_row = i
        
        return pivot_row if max_val > 1e-10 else -1
    
    def _analyze_solution(self, augmented: np.ndarray, m: int, n: int, rank: int, 
                         pivot_cols: List[int]) -> Tuple[Optional[np.ndarray], bool, str]:
        """
        Analiza la matriz escalonada y determina el tipo de solución.
        
        Args:
            augmented: Matriz aumentada escalonada
            m: Número de ecuaciones
            n: Número de variables
            rank: Rango de la matriz de coeficientes
            pivot_cols: Lista de columnas pivote
            
        Returns:
            Tuple con solución, validez y mensaje
        """
        # Verificar consistencia (0 = número ≠ 0)
        for i in range(rank, m):
            if abs(augmented[i, n]) > 1e-10:  # 0 = número ≠ 0
                return None, False, "Sistema inconsistente (sin solución)"
        
        # Determinar tipo de solución
        if rank == n:
            # Solución única
            solution = self._back_substitution(augmented, n, pivot_cols)
            return solution, True, "Solución única encontrada"
        
        elif rank < n:
            # Infinitas soluciones
            if m < n:
                msg = f"Infinitas soluciones: {n-rank} variables libres (sistema subdeterminado)"
            else:
                msg = f"Infinitas soluciones: {n-rank} variables libres (matriz singular)"
            
            # Intentar encontrar una solución particular
            solution = self._find_particular_solution(augmented, n, rank, pivot_cols)
            return solution, False, msg
        
        else:
            return None, False, "Error en análisis de rango"
    
    def _back_substitution(self, augmented: np.ndarray, n: int, pivot_cols: List[int]) -> np.ndarray:
        """
        Realiza sustitución hacia atrás para sistemas con solución única.
        
        Args:
            augmented: Matriz aumentada escalonada
            n: Número de variables
            pivot_cols: Lista de columnas pivote
            
        Returns:
            Vector solución
        """
        solution = np.zeros(n)
        
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            solution[col] = augmented[i, n]  # Término independiente
            
            # Restar contribuciones de variables ya resueltas
            for j in range(col + 1, n):
                solution[col] -= augmented[i, j] * solution[j]
            
            # Dividir por el coeficiente
            solution[col] /= augmented[i, col]
        
        return solution
    
    def _find_particular_solution(self, augmented: np.ndarray, n: int, rank: int, 
                                 pivot_cols: List[int]) -> Optional[np.ndarray]:
        """
        Encuentra una solución particular cuando hay infinitas soluciones.
        
        Args:
            augmented: Matriz aumentada escalonada
            n: Número de variables
            rank: Rango de la matriz
            pivot_cols: Lista de columnas pivote
            
        Returns:
            Una solución particular (variables libres = 0)
        """
        try:
            solution = np.zeros(n)
            
            # Resolver para las variables pivote (variables libres = 0)
            for i in range(rank - 1, -1, -1):
                col = pivot_cols[i]
                solution[col] = augmented[i, n]
                
                for j in range(col + 1, n):
                    solution[col] -= augmented[i, j] * solution[j]
                
                solution[col] /= augmented[i, col]
            
            return solution
            
        except:
            return None
    
    def get_solution_info(self) -> str:
        """
        Proporciona información detallada sobre el tipo de solución.
        
        Returns:
            String con información del sistema
        """
        if not self.steps:
            return "No se ha resuelto ningún sistema"
        
        last_matrix = self.steps[-1]
        m, n_plus_1 = last_matrix.shape
        n = n_plus_1 - 1
        
        info = []
        info.append(f"Sistema: {m} ecuaciones, {n} incógnitas")
        
        if m > n:
            info.append("Tipo: Sobredeterminado (más ecuaciones que incógnitas)")
        elif m < n:
            info.append("Tipo: Subdeterminado (menos ecuaciones que incógnitas)")
        else:
            info.append("Tipo: Cuadrado (igual número de ecuaciones e incógnitas)")
        
        return "\n".join(info)
    
    def get_steps(self) -> List[Tuple[np.ndarray, str]]:
        """
        Retorna los pasos del proceso de eliminación.
        
        Returns:
            Lista de tuplas (matriz, operación)
        """
        return list(zip(self.steps, self.operations))
    
    def format_matrix(self, matrix: np.ndarray, decimals: int = 2) -> str:
        """
        Formatea una matriz para mostrarla de manera legible.
        Adaptado para matrices rectangulares.
        
        Args:
            matrix: Matriz a formatear
            decimals: Número de decimales a mostrar
            
        Returns:
            String con la matriz formateada
        """
        rows = []
        for row in matrix:
            formatted_row = []
            for val in row[:-1]:  # Coeficientes
                formatted_row.append(f"{val:8.{decimals}f}")
            formatted_row.append("  |")
            formatted_row.append(f"{row[-1]:8.{decimals}f}")  # Término independiente
            rows.append(" ".join(formatted_row))
        
        return "\n".join(rows)
