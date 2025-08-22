# src/integration/main_system.py

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from .api import (
    registrar_proyecto_api, listar_proyectos_api, eliminar_proyecto_api,
    analizar_documentacion_api, comparar_archivos_codigo_api
)

class MainApp(tk.Tk):
    """
    Clase principal de la aplicación que gestiona la interfaz gráfica.
    """
    def __init__(self):
        super().__init__()
        self.title("Sistema de Análisis y Gestión")
        self.geometry("800x600")

        # Configurar un estilo ttk para mejorar la apariencia
        style = ttk.Style(self)
        style.configure("TButton", font=("Helvetica", 10), padding=5)
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("Header.TLabel", font=("Helvetica", 16, "bold"))
        
        self.frames = {}
        self.create_frames()
        self.show_frame("main_menu")

    def create_frames(self):
        """Crea y almacena los diferentes frames de la aplicación."""
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Crear los frames principales
        self.frames["main_menu"] = MainMenuFrame(container, self)
        self.frames["gestion"] = ProjectManagementFrame(container, self)
        self.frames["analisis"] = ProjectAnalysisFrame(container, self)
        self.frames["herramientas"] = IndividualToolsFrame(container, self)
        
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, page_name):
        """Muestra el frame seleccionado."""
        frame = self.frames[page_name]
        # Llama a un método 'refresh' si existe, para actualizar datos
        if hasattr(frame, 'refresh'):
            frame.refresh()
        frame.tkraise()

# --- Frames de la Aplicación ---

class MainMenuFrame(tk.Frame):
    """Frame para el menú principal."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = ttk.Label(self, text="Menú Principal", style="Header.TLabel")
        label.pack(pady=20, padx=10)

        # --- CORRECCIÓN AQUÍ ---
        # El error estaba en pasar 'pady' directamente al constructor del botón.
        # Se debe pasar al método .pack() para controlar el espaciado.
        button_width = 30
        
        ttk.Button(self, text="1. Gestionar Proyectos", width=button_width, command=lambda: controller.show_frame("gestion")).pack(pady=5)
        ttk.Button(self, text="2. Analizar un Proyecto", width=button_width, command=lambda: controller.show_frame("analisis")).pack(pady=5)
        ttk.Button(self, text="3. Herramientas Individuales", width=button_width, command=lambda: controller.show_frame("herramientas")).pack(pady=5)
        ttk.Button(self, text="4. Salir", width=button_width, command=controller.quit).pack(pady=5)


class ProjectManagementFrame(tk.Frame):
    """Frame para la gestión de proyectos (CRUD)."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Gestión de Proyectos", style="Header.TLabel")
        label.pack(pady=10)

        # Contenedor para los botones
        button_container = ttk.Frame(self)
        button_container.pack(pady=10)
        ttk.Button(button_container, text="Registrar", command=self.show_register_form).pack(side="left", padx=5)
        ttk.Button(button_container, text="Eliminar", command=self.show_delete_form).pack(side="left", padx=5)
        ttk.Button(button_container, text="Volver", command=lambda: controller.show_frame("main_menu")).pack(side="left", padx=5)

        self.sub_frame = ttk.Frame(self)
        self.sub_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.show_list_projects()

    def refresh(self):
        """Actualiza la vista de la lista de proyectos al mostrar el frame."""
        self.show_list_projects()

    def clear_sub_frame(self):
        for widget in self.sub_frame.winfo_children():
            widget.destroy()

    def show_register_form(self):
        self.clear_sub_frame()
        
        ttk.Label(self.sub_frame, text="Registrar Nuevo Proyecto", font=("Helvetica", 12)).pack(pady=5)
        
        # Usamos grid para un mejor alineamiento
        form_frame = ttk.Frame(self.sub_frame)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        nombre_entry = ttk.Entry(form_frame, width=50)
        nombre_entry.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(form_frame, text="Ruta de Código:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ruta_codigo_entry = ttk.Entry(form_frame, width=50)
        ruta_codigo_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(form_frame, text="Seleccionar", command=lambda: self.select_directory(ruta_codigo_entry)).grid(row=1, column=2, padx=5)

        ttk.Label(form_frame, text="Ruta de Documentación:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ruta_doc_entry = ttk.Entry(form_frame, width=50)
        ruta_doc_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Button(form_frame, text="Seleccionar", command=lambda: self.select_file(ruta_doc_entry, [("PDF files", "*.pdf")])).grid(row=2, column=2, padx=5)

        ttk.Button(self.sub_frame, text="Registrar Proyecto", command=lambda: self.register_project(nombre_entry.get(), ruta_codigo_entry.get(), ruta_doc_entry.get())).pack(pady=20)

    def select_directory(self, entry):
        path = filedialog.askdirectory()
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def select_file(self, entry, filetypes):
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            entry.delete(0, tk.END)
            entry.insert(0, path)

    def register_project(self, nombre, ruta_codigo, ruta_doc):
        if not all([nombre, ruta_codigo, ruta_doc]):
            messagebox.showwarning("Campos incompletos", "Por favor, completa todos los campos.")
            return
        response = registrar_proyecto_api(nombre, ruta_codigo, ruta_doc)
        messagebox.showinfo("Registro de Proyecto", response['message'])
        self.show_list_projects()

    def show_list_projects(self):
        self.clear_sub_frame()
        response = listar_proyectos_api()
        proyectos = response.get('proyectos', [])

        if not proyectos:
            ttk.Label(self.sub_frame, text="No hay proyectos registrados.").pack()
            return
        
        ttk.Label(self.sub_frame, text="Proyectos Registrados:", font=("Helvetica", 12)).pack(pady=5)
        # Usamos un Treeview para una tabla más ordenada
        tree = ttk.Treeview(self.sub_frame, columns=('Nombre', 'Código', 'Documentación'), show='headings')
        tree.heading('Nombre', text='Nombre')
        tree.heading('Código', text='Ruta de Código')
        tree.heading('Documentación', text='Ruta de Documentación')
        tree.column('Nombre', width=150)
        tree.column('Código', width=250)
        tree.column('Documentación', width=250)

        for p in proyectos:
            tree.insert('', tk.END, values=(p['nombre'], p['ruta_codigo'], p['ruta_documento']))
        
        tree.pack(fill="both", expand=True)

    def show_delete_form(self):
        self.clear_sub_frame()
        response = listar_proyectos_api()
        proyectos = response.get('proyectos', [])
        
        if not proyectos:
            ttk.Label(self.sub_frame, text="No hay proyectos para eliminar.").pack()
            return
        
        nombres = [p['nombre'] for p in proyectos]
        
        ttk.Label(self.sub_frame, text="Selecciona el proyecto a eliminar:").pack(pady=5)
        self.delete_combo = ttk.Combobox(self.sub_frame, values=nombres, state="readonly", width=40)
        self.delete_combo.pack(pady=5)
        if nombres:
            self.delete_combo.set(nombres[0])
        
        ttk.Button(self.sub_frame, text="Eliminar Proyecto Seleccionado", command=self.delete_project).pack(pady=10)

    def delete_project(self):
        nombre = self.delete_combo.get()
        if not nombre:
            messagebox.showwarning("Error", "Por favor, selecciona un proyecto.")
            return

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de que quieres eliminar el proyecto '{nombre}'?"):
            response = eliminar_proyecto_api(nombre)
            messagebox.showinfo("Eliminar Proyecto", response['message'])
            self.show_list_projects()


class ProjectAnalysisFrame(tk.Frame):
    """Frame para el análisis de proyectos existentes."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Análisis de Proyectos", style="Header.TLabel")
        label.pack(pady=10)

        # Contenedor para seleccionar proyecto
        ttk.Label(self, text="Selecciona un proyecto:").pack(pady=5)
        self.project_combo = ttk.Combobox(self, values=[], state="readonly", width=50)
        self.project_combo.pack(pady=5)
        
        # Contenedor para las opciones de análisis
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=20)
        ttk.Button(options_frame, text="Analizar Documentación (OBST)", command=self.run_obst).pack(side="left", padx=10)
        ttk.Button(options_frame, text="Comparar Código (LCS)", command=self.run_lcs).pack(side="left", padx=10)

        ttk.Button(self, text="Volver al Menú Principal", command=lambda: controller.show_frame("main_menu")).pack(pady=10)

    def refresh(self):
        """Actualiza la lista de proyectos al mostrar el frame."""
        response = listar_proyectos_api()
        proyectos = response.get('proyectos', [])
        self.nombres_proyectos = [p['nombre'] for p in proyectos]
        self.project_combo['values'] = self.nombres_proyectos
        if self.nombres_proyectos:
            self.project_combo.set(self.nombres_proyectos[0])
        else:
            self.project_combo.set('')

    def run_obst(self):
        nombre_proyecto = self.project_combo.get()
        if not nombre_proyecto:
            messagebox.showwarning("Advertencia", "No hay proyectos para analizar.")
            return
        
        response = analizar_documentacion_api(nombre_proyecto)
        if response['status'] == 'success':
            terminos_str = ', '.join(response['terminos_analizados']) if response['terminos_analizados'] else "Ninguno"
            message = f"Análisis OBST completado para '{response['proyecto']}'.\n\nCosto Óptimo: {response['costo_obst']:.4f}\nTérminos ({len(response['terminos_analizados'])}): {terminos_str}"
            messagebox.showinfo("Resultado Análisis OBST", message)
        else:
            messagebox.showerror("Error de Análisis", response['message'])

    def run_lcs(self):
        nombre_proyecto = self.project_combo.get()
        if not nombre_proyecto:
            messagebox.showwarning("Advertencia", "No hay proyectos para analizar.")
            return
        
        proyectos = listar_proyectos_api().get('proyectos', [])
        proyecto = next((p for p in proyectos if p['nombre'] == nombre_proyecto), None)
        ruta_codigo = proyecto['ruta_codigo'] if proyecto else '.'

        messagebox.showinfo("Selección de Archivos", "A continuación, selecciona los dos archivos a comparar.")
        file1 = filedialog.askopenfilename(title="Selecciona el PRIMER archivo", initialdir=ruta_codigo, filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if not file1: return

        file2 = filedialog.askopenfilename(title="Selecciona el SEGUNDO archivo", filetypes=[("Python files", "*.py"), ("All files", "*.*")])
        if not file2: return

        response = comparar_archivos_codigo_api(file1, file2)
        if response['status'] == 'success':
            lcs_str = ' '.join(response['lcs_sequence']) if response['lcs_sequence'] else "Ninguna"
            message = f"Análisis LCS completado.\n\nSimilitud: {response['similitud']:.2%}\n\nSecuencia Común Más Larga:\n{lcs_str}"
            messagebox.showinfo("Resultado Análisis LCS", message)
        else:
            messagebox.showerror("Error de Análisis", response['message'])


class IndividualToolsFrame(tk.Frame):
    """Frame para las herramientas individuales (OBST y LCS)."""
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = ttk.Label(self, text="Herramientas Individuales", style="Header.TLabel")
        label.pack(pady=10)
        
        options_frame = ttk.Frame(self)
        options_frame.pack(pady=20)
        ttk.Button(options_frame, text="Análisis de Documento (OBST)", command=self.run_individual_obst).pack(side="left", padx=10)
        ttk.Button(options_frame, text="Comparación de Código (LCS)", command=self.run_individual_lcs).pack(side="left", padx=10)

        ttk.Button(self, text="Volver al Menú Principal", command=lambda: controller.show_frame("main_menu")).pack(pady=10)

    def run_individual_obst(self):
        ruta_doc = filedialog.askopenfilename(title="Selecciona un documento PDF", filetypes=[("PDF files", "*.pdf")])
        if not ruta_doc: return

        from ..utils.probability_calculator import obtener_probabilidades_de_documento
        from ..obst.obst import optimal_bst
        
        try:
            terminos, p, q = obtener_probabilidades_de_documento(ruta_doc)
            if not terminos:
                messagebox.showerror("Error", "No se pudieron extraer términos clave del documento.")
                return
            
            costo, _ = optimal_bst(terminos, p, q)
            terminos_str = ', '.join(terminos)
            message = f"Análisis OBST completado.\n\nCosto Óptimo: {costo:.4f}\nTérminos ({len(terminos)}): {terminos_str}"
            messagebox.showinfo("Resultado Análisis OBST", message)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al analizar el documento: {e}")

    def run_individual_lcs(self):
        messagebox.showinfo("Selección de Archivos", "A continuación, selecciona los dos archivos a comparar.")
        file1 = filedialog.askopenfilename(title="Selecciona el PRIMER archivo")
        if not file1: return
        
        file2 = filedialog.askopenfilename(title="Selecciona el SEGUNDO archivo")
        if not file2: return

        response = comparar_archivos_codigo_api(file1, file2)
        if response['status'] == 'success':
            lcs_str = ' '.join(response['lcs_sequence']) if response['lcs_sequence'] else "Ninguna"
            message = f"Análisis LCS completado.\n\nSimilitud: {response['similitud']:.2%}\n\nSecuencia Común Más Larga:\n{lcs_str}"
            messagebox.showinfo("Resultado Análisis LCS", message)
        else:
            messagebox.showerror("Error de Análisis", response['message'])


if __name__ == "__main__":
    # Asegúrate de que el directorio de datos exista
    data_dir = 'data/individual_datasets'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    app = MainApp()
    app.mainloop()