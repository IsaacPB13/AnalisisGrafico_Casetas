#Ventana para las gráficas y descarga imagen y tablas
#PBIU
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import seaborn as sns


#Cambiar por recibir dataframes de la interfaz
#df_compacto = pd.read_excel("pruebaIngresos.xlsx")
#df_extendido = pd.read_excel("pruebaFrecuencias.xlsx")

#Para la gráfica de ingresos, hacerla de barras
#x -> Clases (autipistas y totales)
#y -> Ingreso en pesos $

#Para formatear ingresos
def millones(x, pos):
    return f'{x/1_000_000:.1f}M'

#-----------------------------GRÁFICAS COMPACTADAS-------------------------------
#Grafica de los ingresos por clase compactado
def graficarIngresosClase(df):

    #Agrupar
    df_grouped = df.groupby(['Clase', 'Origen'])['Importe'].sum().reset_index()
    #Pivotar
    df_pivot = df_grouped.pivot(index='Clase', columns='Origen', values='Importe').fillna(0)
    #Agregando total
    df_pivot['Total'] = df_pivot.sum(axis=1)
    #Construyendo el gráfico manualmente
    clases = df_pivot.index.tolist()
    origenes = df_pivot.columns.tolist()
    x = np.arange(len(clases))  # posiciones base (A, B, C)
    width = 0.2  # ancho de cada barra
    #Para la figura
    fig, ax = plt.subplots(figsize=(16,9))
    #Dibujando barras
    for i, origen in enumerate(origenes):
        ax.bar(
            x + i * width,                  # desplazamiento lateral
            df_pivot[origen],              # valores
            width,
            label=origen
        )
    #Centrando eje x
    ax.set_xticks(x + width * (len(origenes)-1) / 2)
    ax.set_xticklabels(clases)

    #Etiquetado
    ax.yaxis.set_major_formatter(FuncFormatter(millones))
    ax.set_xlabel('Afores')
    ax.set_ylabel('Pesos')
    ax.set_title('Ingresos por autopista')
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    #plt.savefig('grafico_ingresos.png', dpi=300, bbox_inches='tight')
    #plt.show()
    #plt.close()
    return fig, df_pivot

#Grafica de las frecuencias por hora compactado
def graficarFrecuenciasHora(df):
    #Formatear para solo tener la hora entera
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.hour
    #Agrupar por origen y clase
    df_freq = df.groupby(['Hora', 'Clase', 'Origen']).size().reset_index(name='Frecuencia')
    #Pivotando para graficar
    df_pivot = df_freq.pivot_table(
        index='Hora',
        columns=['Clase', 'Origen'],
        values='Frecuencia',
        fill_value=0    
    )
    #Graficando lineas de frecuencia por clase
    clases = df['Clase'].unique()

    fig, axes = plt.subplots(len(clases), 1, figsize=(16,9), sharex=True)

    for ax, clase in zip(axes, clases):
        subset = df_freq[df_freq['Clase'] == clase]
        
        pivot = subset.pivot(index='Hora', columns='Origen', values='Frecuencia').fillna(0)
        pivot = pivot.reindex(range(24), fill_value=0)

        for origen in pivot.columns:
            ax.plot(pivot.index, pivot[origen], marker='o', label=origen)

        ax.set_title(f'Clase {clase}')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend()

    axes[-1].set_xlabel('Hora')

    plt.tight_layout()
    fig.canvas.draw()
    #plt.savefig('grafico_frecuencias.png', dpi=300, bbox_inches='tight')
    #plt.show()
    #plt.close()
    return fig, df_pivot

#----------------------------GRAFICAS EXTENDIDAS----------------------------------
#Grafica de frecuencias por hora
def graficarFrecuenciasExtendido(df):
    
    # Asegurar que Hora esté en formato correcto (0-23)
    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.hour
    # Agrupar
    freq = df.groupby(['Origen', 'Hora', 'Clase']).size().reset_index(name='Frecuencia')
    # Obtener lista de origenes
    origenes = freq['Origen'].unique()

    figs = []  
    contador = 1

    for origen in origenes:
        subset = freq[freq['Origen'] == origen]
        
        pivot = subset.pivot(index='Hora', columns='Clase', values='Frecuencia').fillna(0)
        
        fig, ax = plt.subplots(figsize=(16, 9), dpi=300) 
        pivot.plot(ax=ax, kind='line')

        ax.set_title(f'Frecuencia por hora - Origen {origen}')
        ax.set_xlabel('Hora')
        ax.set_ylabel('Frecuencia')
        ax.grid()
        plt.tight_layout()
        
        fig.canvas.draw()

        figs.append(fig) 
        
        #plt.savefig(f'grafico_frecuencias_origen_{contador}.png', dpi=300, bbox_inches='tight')
        #plt.show()
        #plt.close()
        contador += 1
    
    return figs, freq

#Grafica de los ingresos por clase
def graficarIngresosClaseExtendido(df):
    #Agrupando
    df_grouped = df.groupby(['Origen', 'Clase'])['Importe'].sum().reset_index()
    origenes = df_grouped['Origen'].unique()
    figs = []
    contador = 1
    
    for origen in origenes:
        subset = df_grouped[df_grouped['Origen'] == origen]
        
        subset = subset.sort_values('Importe', ascending=False)
        
        fig, ax = plt.subplots()

        ax.bar(subset['Clase'], subset['Importe'])

        ax.yaxis.set_major_formatter(FuncFormatter(millones))

        ax.set_title(f'Ingresos por clase - Origen {origen}')
        ax.set_xlabel('Clase')
        ax.set_ylabel('Ingresos')

        plt.xticks(rotation=45)
        plt.tight_layout()
        #plt.savefig(f'grafico_ingresos_origen_{contador}.png', dpi=300, bbox_inches='tight')
        figs.append(fig)
        contador += 1 
        #plt.show()
        #plt.close()

    return figs, df_grouped

#--------------------------CAMBIAR POR LA VISTA TKINTER----------------------------
#graficarIngresosClase(df_compacto)
#graficarFrecuenciasHora(df_compacto)
#graficarFrecuenciasExtendido(df_extendido)
#graficarIngresosClaseExtendido(df_extendido)