import numpy as np
from typing import Tuple, List, Optional

class GaussElimination:
    
    
    def __init__(self):
        self.steps = []  # Almacena los pasos de la eliminación
        self.operations = []  # Almacena las operaciones realizadas
    
    def solve(self, matrix: np.ndarray, vector: np.ndarray) -> Tuple[Optional[np.ndarray], bool, str]:
        """
        Resuelve el sistema de ecuaciones Ax = b usando eliminación de Gauss.
        
        Args:
            matrix: Matriz de coeficientes A (n x n)
            vector: Vector independiente b (n x 1)
            
        Returns:
            Tuple con:
            - Solución del sistema (None si no tiene solución única)
            - Boolean indicando si tiene solución única
            - Mensaje de error si aplica
        """
        try:
            # Reiniciar pasos y operaciones
            self.steps = []
            self.operations = []
            
            # Crear matriz aumentada
            n = len(matrix)
            augmented = np.column_stack((matrix.astype(float), vector.astype(float)))
            
            # Guardar matriz inicial
            self.steps.append(augmented.copy())
            self.operations.append("Matriz aumentada inicial:")
            
            # Eliminación hacia adelante
            for i in range(n):
                # Buscar pivote
                pivot_row = self._find_pivot(augmented, i)
                
                if pivot_row == -1:
                    return None, False, "Sistema sin solución única (matriz singular)"
                
                # Intercambiar filas si es necesario
                if pivot_row != i:
                    augmented[[i, pivot_row]] = augmented[[pivot_row, i]]
                    self.steps.append(augmented.copy())
                    self.operations.append(f"Intercambiar fila {i+1} con fila {pivot_row+1}")
                
                # Verificar si el pivote es cero
                if abs(augmented[i, i]) < 1e-10:
                    return None, False, "Sistema sin solución única (pivote nulo)"
                
                # Eliminar elementos debajo del pivote
                for j in range(i + 1, n):
                    if abs(augmented[j, i]) > 1e-10:
                        factor = augmented[j, i] / augmented[i, i]
                        augmented[j] = augmented[j] - factor * augmented[i]
                        
                        self.steps.append(augmented.copy())
                        self.operations.append(f"F{j+1} = F{j+1} - ({factor:.2f}) * F{i+1}")
            
            # Sustitución hacia atrás
            solution = np.zeros(n)
            for i in range(n - 1, -1, -1):
                solution[i] = augmented[i, n]
                for j in range(i + 1, n):
                    solution[i] -= augmented[i, j] * solution[j]
                solution[i] /= augmented[i, i]
            
            return solution, True, ""
            
        except Exception as e:
            return None, False, f"Error en el cálculo: {str(e)}"
    
    def _find_pivot(self, matrix: np.ndarray, col: int) -> int:
        """
        Encuentra la fila con el mayor elemento en valor absoluto para usar como pivote.
        
        Args:
            matrix: Matriz aumentada
            col: Columna donde buscar el pivote
            
        Returns:
            Índice de la fila con el mayor pivote, -1 si todos son cero
        """
        n = len(matrix)
        max_val = 0
        pivot_row = -1
        
        for i in range(col, n):
            if abs(matrix[i, col]) > max_val:
                max_val = abs(matrix[i, col])
                pivot_row = i
        
        return pivot_row if max_val > 1e-10 else -1
    
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
