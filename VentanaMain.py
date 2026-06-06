#Graficador de ingresos y frecuencias por hora de casetas. Main Interfaz
#PBIU
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import os
import threading
from Controlador import generarFlujo
from VentanaResultados import VentanaResultados

#Diseño de ventana
class VentanaMain(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)    

        self.etiquetaArchivo = ttk.Label(
            parent, text="Ingrese el archivo a analizar:")
        self.etiquetaArchivo.place(x=20, y=20)
        self.etiquetaNombreArc = ttk.Label(
            parent, text="No hay archivo cargado")
        self.etiquetaNombreArc.place(x=200, y=20)
        self.botonArchivo = tk.Button(
            parent, text="Añadir", command=self.agregaArchivo)
        self.botonArchivo.place(x=80, y=80)
        self.botonEnviar = tk.Button(
            parent, text="Enviar", command=self.enviar)
        self.botonEnviar.place(x=250, y=80)

        #Barra de progreso 
        self.barra = ttk.Progressbar(parent, orient="horizontal", length=300, mode="determinate")
        self.barra.place(x=40, y=50)

    def agregaArchivo(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=(("Archivos de Excel", "*.xlsx"), ("Archivos separados por comas", "*.csv"),("Todos los archivos", "*.*"))
        )

        if not ruta_archivo:
            return  # usuario canceló

        try:
            if ruta_archivo.endswith(".xlsx"):
                self.df = pd.read_excel(ruta_archivo)

            elif ruta_archivo.endswith(".csv"):
                self.df = pd.read_csv(ruta_archivo)

            else:
                raise ValueError("Formato no válido")

            self.ruta_archivo = ruta_archivo
            # Actualizar etiqueta correctamente
            nombre = os.path.basename(ruta_archivo)
            self.etiquetaNombreArc.config(
                text=f"Archivo cargado:\n {nombre}"
            )

        except Exception as e:
            # Regresar a estado inicial
            self.df = None
            self.etiquetaNombreArc.config(
                text="No hay archivo cargado"
            )
            messagebox.showerror(
                title="Error",
                message=f"No se pudo cargar el archivo:\n{e}"
            )

    #MÉTODO ENVIAR ARCHIVO MANDA A LLAMAR A LA CLASE QUE PROCESA EL DATAFRAME
    def enviar(self):

        if not hasattr(self, "ruta_archivo"):
            messagebox.showwarning(
                "Advertencia",
                "No hay archivo cargado"
            )
            return

        def tarea():

            try:

                df1, df2, df3, df4, figs, mes, anio = generarFlujo(
                    self.ruta_archivo,
                    update_progress=self.actualizar_barra
                )

                # Abrir ventana de resultados desde el hilo principal
                self.after(
                    0,
                    lambda: self.mostrar_resultados(
                        df1, df2, df3, df4, figs, mes, anio
                    )
                )

            except Exception as e:

                self.after(
                    0,
                    lambda: messagebox.showerror(
                        "Error",
                        str(e)
                    )
                )

            finally:
                self.after(
                    0,
                    lambda: self.barra.configure(value=0)
                )

        threading.Thread(
            target=tarea,
            daemon=True
        ).start()

    def actualizar_barra(self, valor):
        self.barra["value"] = valor
        self.update_idletasks()

    #PARA LA VENTANA DE LOS RESULTADOS
    def mostrar_resultados(self, df1, df2, df3, df4, figs, mes, anio):

        ventana = tk.Toplevel(self)

        ventana.title("Resultados")
        ventana.geometry("1000x700")

        VentanaResultados(
            ventana,
            df1,
            df2,
            df3,
            df4,
            figs,
            mes,
            anio
        )

app = tk.Tk()
app.title("Graficador. Casetas de autopistas")
app.geometry("375x120")
ventana = VentanaMain(app)
app.mainloop()