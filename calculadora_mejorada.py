#!/usr/bin/env python3


import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from gauss_elimination_mejorado import GaussEliminationMejorado
from gauss_jordan import GaussJordan

class CalculadoraAlgebraMejorada:
    
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Álgebra - Sistema Completo")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Variables del sistema
        self.entradas_matriz = []
        self.entradas_vector = []
        self.metodo_var = tk.StringVar(value="gauss_jordan")
        self.ecuaciones_var = tk.StringVar(value="3")
        self.variables_var = tk.StringVar(value="3")
        
        # Solucionadores
        self.solucionador_gauss = GaussEliminationMejorado()
        self.solucionador_jordan = GaussJordan()
        
        # Colores del tema
        self.colores = {
            'primario': '#2c3e50',
            'secundario': '#3498db', 
            'exito': '#27ae60',
            'advertencia': '#f39c12',
            'error': '#e74c3c',
            'fondo': '#f0f0f0',
            'blanco': '#ffffff',
            'texto': '#2c3e50'
        }
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """Configura la interfaz principal de la aplicación."""
        
        # Título principal
        titulo_frame = tk.Frame(self.root, bg=self.colores['primario'], height=70)
        titulo_frame.pack(fill='x')
        titulo_frame.pack_propagate(False)
        
        titulo_label = tk.Label(
            titulo_frame, 
            text="🧮 CALCULADORA DE SISTEMAS DE ECUACIONES LINEALES 🧮",
            font=('Arial', 18, 'bold'),
            fg='white',
            bg=self.colores['primario']
        )
        titulo_label.pack(expand=True)
        
        # Frame principal
        frame_principal = tk.Frame(self.root, bg=self.colores['fondo'])
        frame_principal.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Configurar grid principal
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=2)
        frame_principal.rowconfigure(0, weight=1)
        
        # Panel izquierdo - Configuración y entrada
        panel_izquierdo = tk.Frame(frame_principal, bg=self.colores['fondo'])
        panel_izquierdo.grid(row=0, column=0, sticky='nsew', padx=(0, 15))
        
        # Panel derecho - Resultados
        panel_derecho = tk.Frame(frame_principal, bg=self.colores['fondo'])
        panel_derecho.grid(row=0, column=1, sticky='nsew')
        
        self.crear_panel_configuracion(panel_izquierdo)
        self.crear_panel_matriz(panel_izquierdo)
        self.crear_panel_botones(panel_izquierdo)
        self.crear_panel_resultados(panel_derecho)
    
    def crear_panel_configuracion(self, padre):
        """Crea el panel de configuración del sistema."""
        
        config_frame = tk.LabelFrame(
            padre, 
            text="⚙️ Configuración del Sistema", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        config_frame.pack(fill='x', pady=(0, 10))
        
        # Frame interno para organización
        frame_interno = tk.Frame(config_frame, bg=self.colores['fondo'])
        frame_interno.pack(fill='x', padx=15, pady=15)
        
        # Dimensiones del sistema
        tk.Label(
            frame_interno, 
            text="Número de ecuaciones (m):", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=0, column=0, sticky='w')
        
        ecuaciones_spin = tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=8, 
            textvariable=self.ecuaciones_var, 
            width=5,
            font=('Arial', 10)
        )
        ecuaciones_spin.grid(row=0, column=1, padx=5)
        
        tk.Label(
            frame_interno, 
            text="Número de variables (n):", 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).grid(row=0, column=2, sticky='w', padx=(20, 0))
        
        variables_spin = tk.Spinbox(
            frame_interno, 
            from_=1, 
            to=8, 
            textvariable=self.variables_var, 
            width=5,
            font=('Arial', 10)
        )
        variables_spin.grid(row=0, column=3, padx=5)
        
        tk.Button(
            frame_interno, 
            text="Actualizar Matriz", 
            command=self.actualizar_matriz,
            bg=self.colores['secundario'], 
            fg='white',
            font=('Arial', 10, 'bold')
        ).grid(row=0, column=4, padx=(20, 0))
        
        # Método de resolución
        metodo_frame = tk.Frame(frame_interno, bg=self.colores['fondo'])
        metodo_frame.grid(row=1, column=0, columnspan=5, sticky='w', pady=(15, 0))
        
        tk.Label(
            metodo_frame, 
            text="Método de resolución:", 
            bg=self.colores['fondo'],
            fg=self.colores['texto'],
            font=('Arial', 10, 'bold')
        ).pack(side='left')
        
        tk.Radiobutton(
            metodo_frame, 
            text="🔸 Gauss (Forma Triangular)", 
            variable=self.metodo_var, 
            value="gauss",
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).pack(side='left', padx=(15, 0))
        
        tk.Radiobutton(
            metodo_frame, 
            text="💎 Gauss-Jordan (Forma Reducida)", 
            variable=self.metodo_var, 
            value="gauss_jordan",
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        ).pack(side='left', padx=(15, 0))
    
    def crear_panel_matriz(self, padre):
        """Crea el panel de entrada de la matriz."""
        
        self.frame_matriz = tk.LabelFrame(
            padre, 
            text="📊 Sistema de Ecuaciones Lineales", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        self.frame_matriz.pack(fill='both', expand=True, pady=(0, 10))
        
        self.actualizar_matriz()
    
    def actualizar_matriz(self):
        """Actualiza la interfaz de entrada de la matriz."""
        
        try:
            m = int(self.ecuaciones_var.get())
            n = int(self.variables_var.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese números válidos para las dimensiones")
            return
        
        if m < 1 or n < 1 or m > 8 or n > 8:
            messagebox.showerror("Error", "Las dimensiones deben estar entre 1 y 8")
            return
        
        # Limpiar frame anterior
        for widget in self.frame_matriz.winfo_children():
            widget.destroy()
        
        # Información del sistema
        info_tipo = self.determinar_tipo_sistema(m, n)
        info_label = tk.Label(
            self.frame_matriz, 
            text=f"📋 Sistema {m}×{n} - {info_tipo}", 
            font=('Arial', 11, 'bold'), 
            fg=self.colores['secundario'], 
            bg=self.colores['fondo']
        )
        info_label.pack(pady=10)
        
        # Frame contenedor de la matriz
        contenedor_entradas = tk.Frame(self.frame_matriz, bg=self.colores['fondo'])
        contenedor_entradas.pack(padx=15, pady=15)
        
        # Crear entradas de la matriz
        self.entradas_matriz = []
        for i in range(m):
            fila = []
            for j in range(n):
                entrada = tk.Entry(
                    contenedor_entradas, 
                    width=8, 
                    justify='center',
                    font=('Arial', 10)
                )
                entrada.grid(row=i, column=j, padx=2, pady=2)
                entrada.insert(0, "0")
                fila.append(entrada)
            
            # Símbolo igual
            tk.Label(
                contenedor_entradas, 
                text="=", 
                font=('Arial', 14, 'bold'),
                bg=self.colores['fondo'],
                fg=self.colores['texto']
            ).grid(row=i, column=n, padx=(10, 5))
            
            # Vector independiente
            entrada_vector = tk.Entry(
                contenedor_entradas, 
                width=8, 
                justify='center', 
                bg='#e8f8f5',
                font=('Arial', 10)
            )
            entrada_vector.grid(row=i, column=n+1, padx=2, pady=2)
            entrada_vector.insert(0, "0")
            fila.append(entrada_vector)
            
            self.entradas_matriz.append(fila)
        
        # Etiquetas de variables
        variables_texto = " + ".join([f"x{i+1}" for i in range(n)]) + " = b"
        tk.Label(
            self.frame_matriz, 
            text=f"Variables: {variables_texto}", 
            font=('Arial', 9), 
            fg='#7f8c8d', 
            bg=self.colores['fondo']
        ).pack(pady=(10, 0))
    
    def determinar_tipo_sistema(self, m, n):
        """Determina el tipo de sistema según las dimensiones."""
        
        if m > n:
            return "SOBREDETERMINADO (más ecuaciones que variables)"
        elif m < n:
            return "SUBDETERMINADO (más variables que ecuaciones)"
        else:
            return "CUADRADO (ecuaciones = variables)"
    
    def crear_panel_botones(self, padre):
        """Crea el panel de botones de acción."""
        
        botones_frame = tk.Frame(padre, bg=self.colores['fondo'])
        botones_frame.pack(fill='x', pady=(0, 10))
        
        # Botón resolver - principal
        tk.Button(
            botones_frame, 
            text="🚀 RESOLVER SISTEMA", 
            command=self.resolver_sistema,
            bg=self.colores['exito'], 
            fg='white', 
            font=('Arial', 12, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10), fill='x', expand=True)
        
        # Botón limpiar
        tk.Button(
            botones_frame, 
            text="🧹 Limpiar", 
            command=self.limpiar_todo,
            bg=self.colores['advertencia'], 
            fg='white', 
            font=('Arial', 11, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left', padx=(0, 10))
        
        # Botón ejemplo
        tk.Button(
            botones_frame, 
            text="📝 Ejemplo", 
            command=self.cargar_ejemplo,
            bg='#9b59b6', 
            fg='white', 
            font=('Arial', 11, 'bold'),
            height=2,
            cursor='hand2'
        ).pack(side='left')
    
    def crear_panel_resultados(self, padre):
        """Crea el panel de resultados con pestañas organizadas."""
        
        frame_resultados = tk.LabelFrame(
            padre, 
            text="📈 Resultados y Análisis Completo", 
            font=('Arial', 12, 'bold'), 
            bg=self.colores['fondo'],
            fg=self.colores['texto']
        )
        frame_resultados.pack(fill='both', expand=True)
        
        # Notebook para organizar resultados
        self.notebook = ttk.Notebook(frame_resultados)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Pestaña 1: Análisis del Sistema
        frame_analisis = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame_analisis, text="🔍 Análisis del Sistema")
        
        self.texto_analisis = scrolledtext.ScrolledText(
            frame_analisis, 
            height=25, 
            font=('Consolas', 10),
            bg='white', 
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.texto_analisis.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 2: Proceso Paso a Paso
        frame_proceso = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame_proceso, text="⚡ Proceso Paso a Paso")
        
        self.texto_proceso = scrolledtext.ScrolledText(
            frame_proceso, 
            height=25, 
            font=('Consolas', 10),
            bg='white', 
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.texto_proceso.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 3: Información Detallada (específica para Gauss-Jordan)
        frame_detalle = tk.Frame(self.notebook, bg='white')
        self.notebook.add(frame_detalle, text="📋 Información Detallada")
        
        self.texto_detalle = scrolledtext.ScrolledText(
            frame_detalle, 
            height=25, 
            font=('Consolas', 10),
            bg='white', 
            fg='#2c3e50',
            wrap=tk.WORD
        )
        self.texto_detalle.pack(fill='both', expand=True, padx=10, pady=10)
    
    def obtener_matriz_y_vector(self):
        """Extrae la matriz de coeficientes y vector independiente de las entradas."""
        
        try:
            m = len(self.entradas_matriz)
            n = len(self.entradas_matriz[0]) - 1
            
            # Matriz de coeficientes
            matriz = np.zeros((m, n))
            for i in range(m):
                for j in range(n):
                    valor = self.entradas_matriz[i][j].get().strip()
                    if valor == '':
                        valor = '0'
                    matriz[i, j] = float(valor)
            
            # Vector independiente
            vector = np.zeros(m)
            for i in range(m):
                valor = self.entradas_matriz[i][n].get().strip()
                if valor == '':
                    valor = '0'
                vector[i] = float(valor)
            
            return matriz, vector
            
        except ValueError:
            raise ValueError("Error al leer los valores. Verifique que todos sean números válidos.")
    
    def resolver_sistema(self):
        """Resuelve el sistema usando el método seleccionado."""
        
        try:
            matriz, vector = self.obtener_matriz_y_vector()
            
            # Seleccionar método de resolución
            if self.metodo_var.get() == "gauss_jordan":
                solucionador = self.solucionador_jordan
                solucion, es_unica, mensaje = solucionador.resolver(matriz, vector)
                metodo_nombre = "Gauss-Jordan"
            else:
                solucionador = self.solucionador_gauss
                solucion, es_unica, mensaje = solucionador.solve(matriz, vector)
                metodo_nombre = "Gauss"
            
            # Mostrar resultados
            self.mostrar_analisis_completo(matriz, vector, solucion, es_unica, mensaje, solucionador, metodo_nombre)
            self.mostrar_proceso_detallado(solucionador, metodo_nombre)
            
            # Mostrar información específica para Gauss-Jordan
            if self.metodo_var.get() == "gauss_jordan":
                self.mostrar_informacion_gauss_jordan(solucionador)
            
            # Cambiar a la pestaña de análisis
            self.notebook.select(0)
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def mostrar_analisis_completo(self, matriz, vector, solucion, es_unica, mensaje, solucionador, metodo_nombre):
        """Muestra el análisis completo del sistema resuelto."""
        
        self.texto_analisis.delete(1.0, tk.END)
        
        resultado = []
        resultado.append("═" * 60)
        resultado.append("ANÁLISIS COMPLETO DEL SISTEMA DE ECUACIONES")
        resultado.append("═" * 60)
        resultado.append("")
        
        # Información básica del sistema
        m, n = matriz.shape
        resultado.append("INFORMACIÓN BÁSICA:")
        resultado.append("─" * 30)
        resultado.append(f"• Número de ecuaciones: {m}")
        resultado.append(f"• Número de variables: {n}")
        resultado.append(f"• Tipo de sistema: {self.determinar_tipo_sistema(m, n)}")
        resultado.append(f"• Método utilizado: {metodo_nombre}")
        resultado.append("")
        
        # Sistema original
        resultado.append("SISTEMA ORIGINAL:")
        resultado.append("─" * 30)
        for i in range(m):
            ecuacion_partes = []
            for j in range(n):
                coef = matriz[i, j]
                if j == 0:
                    if coef == 1:
                        ecuacion_partes.append(f"x{j+1}")
                    elif coef == -1:
                        ecuacion_partes.append(f"-x{j+1}")
                    else:
                        ecuacion_partes.append(f"{coef:.2f}x{j+1}")
                else:
                    if coef > 0:
                        if coef == 1:
                            ecuacion_partes.append(f"+ x{j+1}")
                        else:
                            ecuacion_partes.append(f"+ {coef:.2f}x{j+1}")
                    elif coef < 0:
                        if coef == -1:
                            ecuacion_partes.append(f"- x{j+1}")
                        else:
                            ecuacion_partes.append(f"- {abs(coef):.2f}x{j+1}")
            
            resultado.append(f"  {' '.join(ecuacion_partes)} = {vector[i]:.2f}")
        resultado.append("")
        
        # Análisis específico para Gauss-Jordan
        if metodo_nombre == "Gauss-Jordan" and hasattr(solucionador, 'obtener_informacion_detallada'):
            info_detallada = solucionador.obtener_informacion_detallada()
            resultado.append("ANÁLISIS MATEMÁTICO:")
            resultado.append("─" * 30)
            resultado.append(f"• Rango de la matriz: {info_detallada['rango_matriz']}")
            resultado.append(f"• Rango de la matriz aumentada: {info_detallada['rango_aumentada']}")
            resultado.append(f"• Columnas pivote: {info_detallada['columnas_pivote']}")
            
            if info_detallada['variables_libres']:
                resultado.append(f"• Variables libres: {info_detallada['variables_libres']}")
                resultado.append(f"  (Total: {info_detallada['num_variables_libres']} variables libres)")
                
                # Mostrar ecuaciones de variables libres
                if hasattr(solucionador, 'obtener_ecuaciones_variables_libres'):
                    ecuaciones = solucionador.obtener_ecuaciones_variables_libres(
                        solucionador.pasos[-1][0] if solucionador.pasos else None, n
                    )
                    if ecuaciones:
                        resultado.append("• Ecuaciones de variables libres:")
                        for ecuacion in ecuaciones:
                            resultado.append(f"  {ecuacion}")
            else:
                resultado.append("• Variables libres: Ninguna")
            
            resultado.append(f"• Sistema consistente: {'Sí' if info_detallada['es_consistente'] else 'No'}")
            resultado.append(f"• Tipo de solución: {info_detallada['tipo_sistema'].upper()}")
            resultado.append("")
        
        # Resultado final
        resultado.append("RESULTADO:")
        resultado.append("─" * 30)
        resultado.append(mensaje)
        resultado.append("")
        
        if solucion is not None:
            resultado.append("SOLUCIÓN:")
            resultado.append("─" * 30)
            if not es_unica:
                resultado.append("(Solución particular con variables libres = 0)")
            
            for i, valor in enumerate(solucion):
                resultado.append(f"  x{i+1} = {valor:.4f}")
            
            # Verificación de la solución
            resultado.append("")
            resultado.append("VERIFICACIÓN:")
            resultado.append("─" * 30)
            verificacion = np.dot(matriz, solucion)
            for i in range(len(vector)):
                error = abs(verificacion[i] - vector[i])
                estado = "✓" if error < 1e-10 else "≈"
                resultado.append(f"  Ecuación {i+1}: {verificacion[i]:.4f} = {vector[i]:.4f} {estado}")
        
        resultado.append("")
        resultado.append("═" * 60)
        
        self.texto_analisis.insert(tk.END, "\n".join(resultado))
    
    def mostrar_proceso_detallado(self, solucionador, metodo_nombre):
        """Muestra el proceso paso a paso de la resolución."""
        
        self.texto_proceso.delete(1.0, tk.END)
        
        contenido = []
        contenido.append("═" * 60)
        contenido.append(f"PROCESO PASO A PASO - MÉTODO {metodo_nombre.upper()}")
        contenido.append("═" * 60)
        contenido.append("")
        
        # Obtener pasos del proceso
        if hasattr(solucionador, 'obtener_pasos'):
            pasos = solucionador.obtener_pasos()
        elif hasattr(solucionador, 'get_steps'):
            pasos = solucionador.get_steps()
        else:
            contenido.append("No hay pasos disponibles para mostrar.")
            self.texto_proceso.insert(tk.END, "\n".join(contenido))
            return
        
        for i, (matriz_paso, operacion) in enumerate(pasos):
            contenido.append(f"PASO {i+1}:")
            contenido.append("─" * 20)
            contenido.append(f"Operación: {operacion}")
            contenido.append("")
            contenido.append("Matriz resultante:")
            
            # Formatear matriz
            if hasattr(solucionador, 'formatear_matriz'):
                contenido.append(solucionador.formatear_matriz(matriz_paso))
            elif hasattr(solucionador, 'format_matrix'):
                contenido.append(solucionador.format_matrix(matriz_paso))
            else:
                # Formateo básico si no hay método específico
                for fila in matriz_paso:
                    fila_formateada = []
                    for val in fila[:-1]:
                        fila_formateada.append(f"{val:8.2f}")
                    fila_formateada.append(" |")
                    fila_formateada.append(f"{fila[-1]:8.2f}")
                    contenido.append("  " + " ".join(fila_formateada))
            
            contenido.append("")
            contenido.append("")
        
        contenido.append("═" * 60)
        contenido.append("PROCESO COMPLETADO")
        contenido.append("═" * 60)
        
        self.texto_proceso.insert(tk.END, "\n".join(contenido))
    
    def mostrar_informacion_gauss_jordan(self, solucionador):
        """Muestra información específica y detallada para el método Gauss-Jordan."""
        
        self.texto_detalle.delete(1.0, tk.END)
        
        if not hasattr(solucionador, 'obtener_informacion_detallada'):
            self.texto_detalle.insert(tk.END, "Información detallada no disponible para este método.")
            return
        
        info = solucionador.obtener_informacion_detallada()
        
        contenido = []
        contenido.append("═" * 60)
        contenido.append("INFORMACIÓN DETALLADA - MÉTODO GAUSS-JORDAN")
        contenido.append("═" * 60)
        contenido.append("")
        
        contenido.append("ANÁLISIS ESTRUCTURAL:")
        contenido.append("─" * 30)
        contenido.append(f"• Rango de la matriz de coeficientes: {info['rango_matriz']}")
        contenido.append(f"• Rango de la matriz aumentada: {info['rango_aumentada']}")
        contenido.append(f"• Diferencia de rangos: {info['rango_aumentada'] - info['rango_matriz']}")
        contenido.append("")
        
        contenido.append("COLUMNAS PIVOTE:")
        contenido.append("─" * 30)
        if info['columnas_pivote']:
            contenido.append(f"• Posiciones: {info['columnas_pivote']}")
            contenido.append(f"• Total: {len(info['columnas_pivote'])} columnas pivote")
            contenido.append("• Estas columnas contienen las variables básicas del sistema")
        else:
            contenido.append("• No se encontraron columnas pivote")
        contenido.append("")
        
        contenido.append("VARIABLES LIBRES:")
        contenido.append("─" * 30)
        if info['variables_libres']:
            contenido.append(f"• Variables libres: {info['variables_libres']}")
            contenido.append(f"• Cantidad: {info['num_variables_libres']}")
            contenido.append("• Estas variables pueden tomar cualquier valor real")
            contenido.append("• La solución mostrada asigna valor 0 a las variables libres")
        else:
            contenido.append("• No hay variables libres")
            contenido.append("• Todas las variables están determinadas por el sistema")
        contenido.append("")
        
        contenido.append("CLASIFICACIÓN DEL SISTEMA:")
        contenido.append("─" * 30)
        contenido.append(f"• Consistencia: {'Consistente' if info['es_consistente'] else 'Inconsistente'}")
        contenido.append(f"• Tipo de solución: {info['tipo_sistema'].upper()}")
        
        if info['tipo_sistema'] == 'unico':
            contenido.append("  → El sistema tiene una única solución")
        elif info['tipo_sistema'] == 'infinito':
            contenido.append("  → El sistema tiene infinitas soluciones")
            contenido.append(f"  → Dimensión del espacio de soluciones: {info['num_variables_libres']}")
        else:
            contenido.append("  → El sistema no tiene solución")
        
        contenido.append("")
        
        contenido.append("INTERPRETACIÓN GEOMÉTRICA:")
        contenido.append("─" * 30)
        if info['tipo_sistema'] == 'unico':
            contenido.append("• Las ecuaciones se intersectan en un único punto")
        elif info['tipo_sistema'] == 'infinito':
            if info['num_variables_libres'] == 1:
                contenido.append("• Las ecuaciones definen una línea (infinitos puntos)")
            elif info['num_variables_libres'] == 2:
                contenido.append("• Las ecuaciones definen un plano (infinitos puntos)")
            else:
                contenido.append(f"• Las ecuaciones definen un hiperplano de dimensión {info['num_variables_libres']}")
        else:
            contenido.append("• Las ecuaciones son contradictorias (no hay intersección)")
        
        contenido.append("")
        contenido.append("═" * 60)
        contenido.append("ANÁLISIS COMPLETADO")
        contenido.append("═" * 60)
        
        self.texto_detalle.insert(tk.END, "\n".join(contenido))
    
    def limpiar_todo(self):
        """Limpia todas las entradas y resultados."""
        
        # Limpiar entradas de la matriz
        for fila in self.entradas_matriz:
            for entrada in fila:
                entrada.delete(0, tk.END)
                entrada.insert(0, "0")
        
        # Limpiar áreas de resultados
        self.texto_analisis.delete(1.0, tk.END)
        self.texto_proceso.delete(1.0, tk.END)
        self.texto_detalle.delete(1.0, tk.END)
        
        # Mensaje de confirmación
        messagebox.showinfo("Limpieza", "Todos los campos han sido limpiados")
    
    def cargar_ejemplo(self):
        """Carga un ejemplo según las dimensiones del sistema actual."""
        
        m = int(self.ecuaciones_var.get())
        n = int(self.variables_var.get())
        
        # Ejemplos predefinidos según el tipo de sistema
        ejemplos = {
            (2, 2): {
                "matriz": [[2, 3], [1, -1]], 
                "vector": [8, 1],
                "descripcion": "Sistema 2×2 con solución única"
            },
            (3, 3): {
                "matriz": [[2, 1, -1], [1, -1, 2], [3, 2, 1]], 
                "vector": [8, 0, 11],
                "descripcion": "Sistema 3×3 con solución única"
            },
            (3, 2): {
                "matriz": [[1, 2], [2, 1], [1, 1]], 
                "vector": [5, 4, 3],
                "descripcion": "Sistema sobredeterminado (puede no tener solución)"
            },
            (2, 3): {
                "matriz": [[1, 2, 3], [2, 1, 1]], 
                "vector": [6, 4],
                "descripcion": "Sistema subdeterminado (infinitas soluciones)"
            },
            (4, 4): {
                "matriz": [[1, 2, -1, 3], [2, -1, 1, 1], [1, -1, 2, -1], [3, 1, -2, 2]], 
                "vector": [10, 8, 5, 12],
                "descripcion": "Sistema 4×4 con solución única"
            }
        }
        
        if (m, n) in ejemplos:
            ejemplo = ejemplos[(m, n)]
            
            # Cargar datos del ejemplo
            for i in range(m):
                for j in range(n):
                    self.entradas_matriz[i][j].delete(0, tk.END)
                    self.entradas_matriz[i][j].insert(0, str(ejemplo["matriz"][i][j]))
                
                # Cargar vector independiente
                self.entradas_matriz[i][n].delete(0, tk.END)
                self.entradas_matriz[i][n].insert(0, str(ejemplo["vector"][i]))
            
            messagebox.showinfo(
                "Ejemplo Cargado", 
                f"Se cargó un ejemplo {m}×{n}:\n{ejemplo['descripcion']}"
            )
        else:
            messagebox.showinfo(
                "Sin Ejemplo", 
                f"No hay ejemplo predefinido para un sistema {m}×{n}.\n"
                "Puede crear su propio ejemplo o cambiar las dimensiones."
            )


def main():
    """Función principal de la aplicación."""
    root = tk.Tk()
    aplicacion = CalculadoraAlgebraMejorada(root)
    root.mainloop()


if __name__ == "__main__":
    main()
