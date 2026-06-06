#Ventana de resultados del análisis. PBIU

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path

#Diseño de la ventana
class VentanaResultados(ttk.Frame):

    def __init__(self, parent, df1, df2, df3, df4, figs, mes, anio):

        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # Guardar referencias
        self.df1 = df1
        self.df2 = df2
        self.df3 = df3
        self.df4 = df4
        self.figs = figs
        self.mes = mes
        self.anio = anio
        self.indice = 0

        # ================= BOTONES =================
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="Descargar tablas",
            command=self.descargarTablas
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            frame_botones,
            text="Descargar gráficas",
            command=self.descargarGraficas
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            frame_botones,
            text="<--",
            command=self.moverIzquierda
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            frame_botones,
            text="-->",
            command=self.moverDerecha
        ).grid(row=0, column=4, padx=5)

        # ================= AREA GRAFICA =================
        self.frameGrafica = tk.Frame(self)
        self.frameGrafica.pack(
            fill="both",
            expand=True
        )

        self.canvas = None

        self.actualizar_grafica()

    # ==================================================
    # MOSTRAR GRAFICA
    # ==================================================
    def actualizar_grafica(self):

        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig = self.figs[self.indice]

        self.canvas = FigureCanvasTkAgg(
            fig,
            master=self.frameGrafica
        )

        self.canvas.draw()

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # ==================================================
    # NAVEGACION
    # ==================================================

    def moverDerecha(self):

        if self.indice < len(self.figs) - 1:
            self.indice += 1
            self.actualizar_grafica()

    def moverIzquierda(self):

        if self.indice > 0:
            self.indice -= 1
            self.actualizar_grafica()

    # ==================================================
    # DESCARGAR TABLAS
    # ==================================================

    def descargarTablas(self):

        directorio = Path.home() / "Desktop"

        self.df1.to_excel(
            directorio / f"tabla_ingresos_compactos_{self.mes}_{self.anio}.xlsx"
        )

        self.df2.to_excel(
            directorio / f"tabla_frecuencias_compactos_{self.mes}_{self.anio}.xlsx"
        )

        self.df3.to_excel(
            directorio / f"tabla_ingresos_extendido_{self.mes}_{self.anio}.xlsx"
        )

        self.df4.to_excel(
            directorio / f"tabla_frecuencias_extendido_{self.mes}_{self.anio}.xlsx"
        )

        messagebox.showinfo(
            "Aviso",
            "Tablas generadas con éxito."
        )

    # ==================================================
    # DESCARGAR GRAFICAS
    # ==================================================

    def descargarGraficas(self):

        directorio = Path.home() / "Desktop"

        for i, fig in enumerate(self.figs, start=1):

            ruta = directorio / f"Grafica_{i}_{self.mes}_{self.anio}.png"

            fig.savefig(
                ruta,
                dpi=300,
                bbox_inches="tight"
            )

        messagebox.showinfo(
            "Aviso",
            "Gráficas generadas con éxito."
        )