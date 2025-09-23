# Calculadora de Álgebra - Eliminación de Gauss

Programa en Python para resolver sistemas de ecuaciones lineales utilizando el método de eliminación de Gauss con interfaz gráfica intuitiva.

## 🎆 Características

### 🌟 **CALCULADORA MEJORADA v2.0 - ACTUALIZADA**
- **Interfaz Completamente en Español**: Todo el código y mensajes traducidos
- **Código Limpio**: Sin emojis en variables/funciones, solo en interfaz
- **Análisis Avanzado de Gauss-Jordan**: 
  - 📍 Detección automática de **columnas pivote** (mostradas con {})
  - 🔄 **Variables libres como ecuaciones** (ej: x₃ = 2x₁ + 3x₂) 
  - 🎥 Clasificación mejorada: **único, infinito o inconsistente**
  - 📈 Verificación de matriz identidad para determinar inconsistencia
  - 📈 Análisis de rangos (matriz y aumentada)
  - 🔍 Interpretación geométrica del sistema
- **3 Pestañas de Resultados**:
  - 🔍 **Análisis del Sistema**: Información completa
  - ⚡ **Proceso Paso a Paso**: Eliminación detallada  
  - 📋 **Información Detallada**: Específica para Gauss-Jordan
- **Soporte de Matrices Rectangulares**: Sistemas m×n (cualquier dimensión)
- **Ejemplos Integrados**: Para diferentes tipos de sistemas

### 🔢 **NUEVA: OPERACIONES MATRICIALES**
- **Suma de Matrices**: A + B con validación de dimensiones
- **Multiplicación de Matrices**: A × B con verificación automática
- **Ejemplos Integrados**: Casos predefinidos para pruebas
- **Interfaz Intuitiva**: Configuración fácil de dimensiones
- **Resultados Detallados**: Muestra proceso y resultado final

### 🚀 **NUEVO: SISTEMA UNIFICADO - ¡LA MEJOR OPCIÓN!**
- **🔄 Navegación Sin Cerrar**: Cambia entre interfaces sin reiniciar
- **🎨 Barra de Navegación**: Botones intuitivos en la parte superior
- **🧮 + 🔢 Todo en Uno**: Acceso completo a ambas funcionalidades
- **💾 Memoria Persistente**: Mantiene los datos al cambiar interfaces
- **🎨 Interfaz Moderna**: Diseño unificado y profesional

### **Características Originales Mejoradas**
- **Método de Eliminación de Gauss**: Implementación completa del algoritmo con pivoteo parcial
- **Método de Gauss-Jordan**: Reducción completa hasta matriz identidad
- **Interfaz Gráfica**: Interfaz amigable desarrollada con Tkinter
- **Proceso Paso a Paso**: Visualización detallada de cada iteración del algoritmo
- **Validación de Entradas**: Verificación automática de valores numéricos
- **Manejo de Errores**: Detección de sistemas sin solución única
- **Resultados Precisos**: Mostrar resultados con 4 decimales de precisión
- **Verificación Automática**: Comprobación de la solución obtenida

##  Requisitos

- **Python 3.7 o superior**
- **NumPy**: Para cálculos matriciales
- **Tkinter**: Para la interfaz gráfica (incluido por defecto en Python)

##  Instalación

1. **Clonar o descargar** los archivos del proyecto
2. **Instalar NumPy** (si no está instalado):
   ```bash
   pip install numpy
   ```
3. **Verificar que Tkinter esté disponible** (normalmente viene incluido con Python)

##  Estructura del Proyecto

```
Calculadora_de_algebra/
├── main.py                       # 🚀 Menú principal de selección
├── 🚀 sistema_unificado.py         # ⭐ NUEVO: Sistema con navegación fluida
├── 🧮 calculadora_mejorada.py      # Calculadora Mejorada v2.0
├── 🔢 operaciones_matriciales.py   # Suma y multiplicación de matrices
├── gauss_jordan.py               # Algoritmo Gauss-Jordan actualizado
├── gauss_elimination_mejorado.py # Algoritmo Gauss para matrices rectangulares
├── calculadora_unificada.py      # Sistema completo original (backup)
├── calculator_gui.py             # Interfaz básica (backup)
├── modern_calculator_gui.py      # Interfaz moderna (backup)
├── gauss_elimination.py          # Algoritmo básico (backup)
├── diagnostico.py                # Herramienta de diagnóstico
├── prueba_gauss_jordan.py        # Pruebas del algoritmo
├── prueba_cambios_nuevos.py      # Pruebas de nuevas funcionalidades
├── README.md                     # Documentación completa
└── requirements.txt              # Dependencias (solo NumPy)
```

##  Uso

### Ejecutar el Programa

```bash
python main.py
```

**Opciones disponibles:**
1. 🚀 **SISTEMA UNIFICADO** → Navegación fluida entre todas las funcionalidades
2. 🧮 **CALCULADORA MEJORADA v2.0** → Solo sistemas de ecuaciones lineales
3. 🔢 **OPERACIONES MATRICIALES** → Solo suma y multiplicación de matrices

### Ejecutar Directamente las Aplicaciones

```bash
# RECOMENDADO: Sistema unificado (navegar sin cerrar)
python sistema_unificado.py

# O individualmente:
python calculadora_mejorada.py      # Solo sistemas de ecuaciones
python operaciones_matriciales.py   # Solo operaciones matriciales
```

### Interfaz de Usuario

1. **Seleccionar número de ecuaciones**: Use el control deslizante o ingrese directamente (2-6 ecuaciones)
2. **Ingresar coeficientes**: Complete la matriz de coeficientes y el vector independiente
3. **Resolver sistema**: Presione el botón "Resolver Sistema"
4. **Ver resultados**: El área inferior mostrará el proceso completo paso a paso

### Funcionalidades Adicionales

- **Botón "Ejemplo"**: Carga un ejemplo predefinido para probar
- **Botón "Limpiar Resultados"**: Limpia el área de resultados
- **Validación en tiempo real**: Los campos se marcan en rojo si contienen valores inválidos

##  Ejemplo de Uso

### Sistema de Ecuaciones 3x3:
```
3x₁ + 2x₂ - x₃ = 1
2x₁ - 2x₂ + 4x₃ = 0  
-x₁ + 0.5x₂ - x₃ = 0
```

### Matriz de Coeficientes:
```
| 3   2  -1 |   | 1 |
| 2  -2   4 | = | 0 |
|-1 0.5 -1 |   | 0 |
```

##  Validaciones y Errores

### Validaciones de Entrada
- **Valores numéricos**: Solo se aceptan números (enteros o decimales)
- **Campos completos**: Todos los campos deben estar llenos
- **Dimensiones correctas**: La matriz debe tener las dimensiones especificadas

### Manejo de Errores
- **Sistema sin solución única**: Detección de matrices singulares
- **Pivote nulo**: Identificación de pivotes cero
- **Entrada inválida**: Mensajes claros de error con `messagebox.showerror`

### Mensajes de Error Típicos
```
"Ingrese únicamente valores numéricos."
"Sistema sin solución única (matriz singular)"
"Sistema sin solución única (pivote nulo)"
```

##  Proceso de Eliminación

El programa muestra:
1. **Sistema original**: Ecuaciones formateadas
2. **Matriz aumentada inicial**: Estado inicial del sistema
3. **Proceso paso a paso**: Cada operación de fila realizada
4. **Matriz triangular superior**: Estado final tras eliminación
5. **Solución**: Valores de las variables con 4 decimales
6. **Verificación**: Comprobación de la solución obtenida

##  Algoritmo Implementado

### Método de Eliminación de Gauss con Pivoteo Parcial:
1. **Formación de matriz aumentada**: [A|b]
2. **Búsqueda de pivote**: Mayor elemento en valor absoluto
3. **Intercambio de filas**: Si es necesario
4. **Eliminación hacia adelante**: Crear matriz triangular superior
5. **Sustitución hacia atrás**: Calcular valores de las variables

##  Características Técnicas

- **Precisión numérica**: Tolerancia de 1e-10 para comparaciones
- **Pivoteo parcial**: Mejora la estabilidad numérica
- **Formato de salida**: 2 decimales de precisión
- **Interfaz responsiva**: Redimensionable y centrada
- **Código modular**: Separación clara entre lógica y presentación

##  Soporte

Si encuentra algún problema:

### Problemas Comunes y Soluciones:

**1. El programa no inicia correctamente**
- **Solución:** Use directamente: `python calculadora_mejorada.py`
- **Alternativa:** Ejecute el diagnóstico: `python diagnostico.py`

**2. Error de dependencias**
- Verifique que Python y NumPy estén correctamente instalados
- Ejecute: `pip install numpy`

**3. Problemas de importación**
- Asegúrese de que todos los archivos estén en la misma carpeta
- Ejecute el diagnóstico: `python diagnostico.py`

**4. Ejecución directa de interfaces**
Si persisten problemas, ejecute directamente:
```bash
python calculator_gui.py                    # Interfaz básica
python calculator_gui_mejorado.py           # Con matrices rectangulares  
python modern_calculator_gui.py             # Interfaz moderna (Gauss & Gauss-Jordan)
```

### Archivo de Diagnóstico:
- `diagnostico.py` - Ejecuta un diagnóstico completo del sistema
- `calculadora_mejorada.py` - Nueva calculadora principal mejorada

##  Notas Técnicas

- **Rango de ecuaciones**: 2 a 6 ecuaciones (configurable)
- **Tipo de números**: Soporta enteros y decimales (positivos y negativos)
- **Separador decimal**: Use punto (.) como separador decimal
- **Memoria**: Optimizado para sistemas pequeños a medianos

---

**Desarrollado con Python, NumPy y Tkinter**
*Implementación educativa del método de eliminación de Gauss*
