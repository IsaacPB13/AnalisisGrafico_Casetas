#Módulo controlador de la interfaz. PBIU
#Importar módulos para el procesamiento
import pandas as pd
from Modulo_TrataDatos import validandoTabla
from Modulo_TrataDatos import formatearDf
from GraficasImg import graficarIngresosClase
from GraficasImg import graficarIngresosClaseExtendido
from GraficasImg import graficarFrecuenciasHora
from GraficasImg import graficarFrecuenciasExtendido
from tkinter import messagebox

#Haciendo el flujo de trabajo
def generarFlujo(ruta_archivo, update_progress):
    # Paso 1: validación y tratamiento
    update_progress(20)
    df = pd.read_excel(ruta_archivo) #Leyendo archivo
    bandera = validandoTabla(df)
    if bandera==True:
        df_compacto, df_extenso = formatearDf(df)  
        # Paso 2: generación de gráficas
        update_progress(60)
        figs_totales = []
        figs_compactas = []
        
        #Para las tablas compactas
        fig_compacta1, tabla_Ingresos = graficarIngresosClase(df_compacto)
        fig_compacta2, tabla_frecuencias = graficarFrecuenciasHora(df_compacto) 
        figs_compactas.append(fig_compacta1) 
        figs_compactas.append(fig_compacta2) 
        
        #Para las tablas extendidas
        figs_extendidas1, tabla_Ingresos_ext = graficarIngresosClaseExtendido(df_extenso)
        figs_extendidas2, tabla_frecuencias_ext = graficarFrecuenciasExtendido(df_extenso)
        for grafica in figs_compactas+figs_extendidas1+figs_extendidas2:
            figs_totales.append(grafica)
        
        # Paso 3: listo
        update_progress(100)
        return tabla_Ingresos, tabla_frecuencias, tabla_Ingresos_ext, tabla_frecuencias_ext, figs_totales
        #RETORNAR A LA INTERFAZ
    else:
        messagebox.showerror(
                title="Error",
                message="Archivo no válido para el análisis, ingresar nuevo archivo"
        )
        update_progress(0)