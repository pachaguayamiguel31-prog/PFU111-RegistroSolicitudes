import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import csv

# Nombre del archivo donde se guardarán los datos
ARCHIVO_DATOS = "solicitudes.csv"

def limpiar_formulario():
    """Restablece todos los campos del formulario a su estado inicial."""
    txt_nombre.delete(0, tk.END)
    txt_codigo.delete(0, tk.END)
    cmb_tipo.set("")
    txt_descripcion.delete("1.0", tk.END)
    cmb_prioridad.set("")
    txt_resultados.config(state=tk.NORMAL)
    txt_resultados.delete("1.0", tk.END)
    txt_resultados.config(state=tk.DISABLED)

def registrar_solicitud():
    """Valida los campos y guarda la solicitud en el archivo CSV."""
    nombre = txt_nombre.get().strip()
    codigo = txt_codigo.get().strip()
    tipo = cmb_tipo.get()
    descripcion = txt_descripcion.get("1.0", tk.END).strip()
    prioridad = cmb_prioridad.get()
    
    # Misión 2: Implementar las validaciones
    errores = []
    if not nombre:
        errores.append("- El nombre del solicitante no puede estar vacío.")
    if not codigo:
        errores.append("- El código de estudiante no puede estar vacío.")
    if tipo not in ["equipo", "software", "conectividad"]:
        errores.append("- Debe seleccionar un tipo de solicitud válido.")
    if not descripcion:
        errores.append("- La descripción del problema no puede estar vacía.")
    if prioridad not in ["bajo", "medio", "alto"]:
        errores.append("- Debe seleccionar una prioridad válida.")
        
    if errores:
        mensaje_error = "Errores de validación:\n" + "\n".join(errores)
        messagebox.showerror("Error de Validación", mensaje_error)
        return

    # Misión 3: Implementar el manejo de archivos (Escritura)
    try:
        archivo_nuevo = not os.path.exists(ARCHIVO_DATOS)
        
        with open(ARCHIVO_DATOS, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Si el archivo es nuevo, escribe la cabecera
            if archivo_nuevo:
                writer.writerow(["nombre", "codigo", "tipo", "descripcion", "prioridad"])
            
            # Guardar el registro
            writer.writerow([nombre, codigo, tipo, descripcion, prioridad])
            
        messagebox.showinfo("Éxito", "Solicitud registrada correctamente.")
        limpiar_formulario()
        
    except Exception as e:
        messagebox.showerror("Error de Archivo", f"No se pudo escribir en el archivo: {e}")

def consultar_solicitudes():
    """Misión 3: Lee el archivo CSV y muestra los registros en el área de texto."""
    txt_resultados.config(state=tk.NORMAL)
    txt_resultados.delete("1.0", tk.END)
    
    # Validar si el archivo existe
    if not os.path.exists(ARCHIVO_DATOS):
        txt_resultados.insert(tk.END, "No existen registros guardados (El archivo 'solicitudes.csv' no existe).\n")
        txt_resultados.config(state=tk.DISABLED)
        messagebox.showwarning("Información", "No hay solicitudes registradas aún.")
        return

    try:
        with open(ARCHIVO_DATOS, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            cabecera = next(reader, None) # Saltar la cabecera
            
            registros = list(reader)
            if not registros:
                txt_resultados.insert(tk.END, "El archivo está vacío.\n")
            else:
                txt_resultados.insert(tk.END, f"{'Nombre':<20} | {'Código':<12} | {'Tipo':<12} | {'Prioridad':<10} | {'Descripción'}\n")
                txt_resultados.insert(tk.END, "-" * 80 + "\n")
                for fila in registros:
                    if len(fila) == 5:
                        nom, cod, tip, desc, pri = fila
                        txt_resultados.insert(tk.END, f"{nom:<20} | {cod:<12} | {tip:<12} | {pri:<10} | {desc}\n")
                        
    except Exception as e:
        messagebox.showerror("Error de Archivo", f"Ocurrió un error al leer el archivo: {e}")
        txt_resultados.insert(tk.END, f"Error al leer los datos: {e}\n")
        
    txt_resultados.config(state=tk.DISABLED)

ventana = tk.Tk()
ventana.title("Registro de Solicitudes de Soporte Técnico")
ventana.geometry("650x600")
ventana.resizable(False, False)

frame_form = ttk.LabelFrame(ventana, text=" Datos de la Solicitud ", padding=15)
frame_form.pack(fill="x", padx=15, pady=10)

ttk.Label(frame_form, text="Nombre del Solicitante:").grid(row=0, column=0, sticky="w", pady=5)
txt_nombre = ttk.Entry(frame_form, width=40)
txt_nombre.grid(row=0, column=1, columnspan=2, sticky="w", pady=5)

ttk.Label(frame_form, text="Código de Estudiante:").grid(row=1, column=0, sticky="w", pady=5)
txt_codigo = ttk.Entry(frame_form, width=40)
txt_codigo.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

ttk.Label(frame_form, text="Tipo de Solicitud:").grid(row=2, column=0, sticky="w", pady=5)
cmb_tipo = ttk.Combobox(frame_form, values=["equipo", "software", "conectividad"], state="readonly", width=37)
cmb_tipo.grid(row=2, column=1, columnspan=2, sticky="w", pady=5)

ttk.Label(frame_form, text="Prioridad:").grid(row=3, column=0, sticky="w", pady=5)
cmb_prioridad = ttk.Combobox(frame_form, values=["bajo", "medio", "alto"], state="readonly", width=37)
cmb_prioridad.grid(row=3, column=1, columnspan=2, sticky="w", pady=5)

ttk.Label(frame_form, text="Descripción del problema:").grid(row=4, column=0, sticky="nw", pady=5)
txt_descripcion = tk.Text(frame_form, height=4, width=38, font=("TkDefaultFont", 10))
txt_descripcion.grid(row=4, column=1, columnspan=2, sticky="w", pady=5)

# Contenedor de Botones
frame_botones = ttk.Frame(ventana)
frame_botones.pack(fill="x", padx=15, pady=5)

btn_registrar = ttk.Button(frame_botones, text="Registrar solicitud", command=registrar_solicitud)
btn_registrar.pack(side="left", padx=5, expand=True, fill="x")

btn_consultar = ttk.Button(frame_botones, text="Consultar solicitudes", command=consultar_solicitudes)
btn_consultar.pack(side="left", padx=5, expand=True, fill="x")

btn_limpiar = ttk.Button(frame_botones, text="Limpiar formulario", command=limpiar_formulario)
btn_limpiar.pack(side="left", padx=5, expand=True, fill="x")

frame_resultados = ttk.LabelFrame(ventana, text=" Consultas y Mensajes del Sistema ", padding=10)
frame_resultados.pack(fill="both", expand=True, padx=15, pady=10)

txt_resultados = tk.Text(frame_resultados, wrap="none", font=("Consolas", 10), state=tk.DISABLED)
txt_resultados.pack(fill="both", expand=True)

ventana.mainloop()