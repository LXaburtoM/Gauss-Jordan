# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based Linear Algebra Calculator that implements Gaussian elimination for solving systems of linear equations. The project features multiple GUI interfaces built with Tkinter and supports both square and rectangular matrix systems.

## Common Commands

### Running the Application

```bash
# Main application (opens interface selector)
python main.py

# Run specific interfaces directly
python calculator_gui.py                    # Classic interface (square matrices only)
python calculator_gui_mejorado.py           # Enhanced interface (supports rectangular matrices)
python modern_calculator_gui.py             # Modern interface with advanced styling

# Run tests
python test_gauss.py                        # Basic algorithm tests
```

### Development and Testing

```bash
# Install dependencies
pip install numpy

# Run specific test/demo scripts
python pasos_detallados.py                  # Step-by-step elimination demo
python probar_casos_especiales.py           # Special cases testing
python probar_matrices_rectangulares.py     # Rectangular matrix testing
python resolver_sistema_especifico.py       # Specific system solver
python comportamiento_detallado.py          # Detailed behavior analysis

# Check dependencies
python -c "import numpy; print(f'NumPy {numpy.__version__} installed')"
python -c "import tkinter; print('Tkinter available')"
```

## Architecture Overview

### Core Components

**Gaussian Elimination Engines:**
- `GaussElimination` (gauss_elimination.py) - Standard implementation for square matrices with partial pivoting
- `GaussEliminationMejorado` (gauss_elimination_mejorado.py) - Enhanced version supporting rectangular matrices (m×n), overdetermined and underdetermined systems

**GUI Applications:**
- `AlgebraCalculator` (calculator_gui.py) - Basic Tkinter interface for square systems
- `CalculadoraAlgebraGUI` (calculator_gui_mejorado.py) - Enhanced interface supporting rectangular matrices with system type analysis
- `ModernAlgebraCalculator` (modern_calculator_gui.py) - Advanced interface with modern styling, tabbed results, and improved UX

**Main Entry Point:**
- `main.py` - Launcher with interface selection dialog and dependency checking

### Key Architecture Patterns

**Algorithm-GUI Separation:** Clean separation between numerical algorithms and presentation layers. Each GUI can use either Gaussian elimination engine.

**Step Tracking:** Both elimination engines maintain detailed step-by-step history of operations through `steps` and `operations` lists, enabling educational visualization.

**Matrix Type Support:**
- Square matrices (n×n) - Standard linear systems
- Rectangular matrices (m×n where m≠n) - Overdetermined/underdetermined systems
- Automatic system type detection and appropriate solution strategies

**Solution Categories:**
- Unique solutions (rank = n)
- Infinite solutions with particular solution (rank < n, consistent)
- No solutions (inconsistent systems)

### Data Flow

1. **Input Validation:** GUI validates numeric input with real-time feedback
2. **Matrix Construction:** Coefficients + independent vector → augmented matrix
3. **Gaussian Elimination:** Forward elimination with partial pivoting + back substitution
4. **Solution Analysis:** Rank analysis determines solution type
5. **Result Display:** Formatted output showing original system, elimination steps, and solutions

### Testing Strategy

The codebase includes multiple test files focusing on:
- **Algorithm Correctness:** `test_gauss.py` validates basic functionality
- **Special Cases:** `probar_casos_especiales.py` tests edge cases (singular matrices, inconsistent systems)
- **Rectangular Matrices:** `probar_matrices_rectangulares.py` validates enhanced functionality
- **Educational Demos:** Various scripts show step-by-step elimination processes

## Dependencies

- **Python 3.7+** - Base language
- **NumPy** - Matrix operations and numerical computations
- **Tkinter** - GUI framework (included with Python)

The `requirements.txt` specifies only NumPy as external dependency. Main.py includes dependency checking with helpful error messages.

## File Organization

- **Core Algorithms:** `gauss_elimination.py`, `gauss_elimination_mejorado.py`
- **GUI Interfaces:** `calculator_gui.py`, `calculator_gui_mejorado.py`, `modern_calculator_gui.py`  
- **Testing:** `test_gauss.py` + various `probar_*.py` and demo scripts
- **Entry Points:** `main.py` (primary), individual GUI files (direct)
- **Documentation:** `README.md` (user guide), this `WARP.md` (dev guide)

## Key Implementation Details

**Numerical Stability:** Uses partial pivoting and 1e-10 tolerance for zero comparisons to handle floating-point precision issues.

**User Experience:** All GUIs include input validation, error messaging, example loading, and results verification.

**Educational Focus:** The step-by-step tracking and detailed process visualization make this particularly suitable for learning linear algebra concepts.

**Multi-Interface Design:** Three different GUI complexity levels accommodate different user needs from basic usage to advanced analysis.
