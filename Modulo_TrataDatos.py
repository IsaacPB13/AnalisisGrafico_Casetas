#Modulo de tratamiento de datos. 
# PBIU

import pandas as pd
"""
Pasos necesarios para el tratamiento

1) Validar columnas del excel/csv
2) Filtrar solo las columnas de interés (origen, fecha, hora, clase, importe)
3) Homologar el formato de la hora
4) Generar una copia de la nueva tabla
5a) A la primera copia se unifican las diversas clases
5b) La segunda se trabaja con todas las variantes
"""

#Función para validar el contenido del xlsx o csv ---------------------------
def validandoTabla(df):
    nombre_columnas = df.columns.tolist()

    if(len(nombre_columnas)!=12): #Validando columnas por cantidad de columnas
        bandera_valida_tamaño = False
        return bandera_valida_tamaño
    else:
        bandera_validar_nombre = True
        for i in range(len(nombre_columnas)): #Validando columnas por nombres
            match nombre_columnas[i]:
                case "Autopista":
                    continue
                case "Origen":
                    continue
                case "Destino":
                    continue
                case "Vía":
                    continue
                case "Modalidad_Vía":
                    continue
                case "Fecha":
                    continue
                case "Hora":
                    continue
                case "Evento":
                    continue
                case "Modo_de_Pago":
                    continue
                case "TAG":
                    continue
                case "Clase":
                    continue
                case "Importe":
                    continue
                case _:
                    bandera_validar_nombre=False
        return bandera_validar_nombre

#Función para formatear el contenido de la tabla para graficar
def formatearDf(df):
    df_filtrado = df.filter(items=["Origen", "Fecha", "Hora", "Clase", "Importe"])#Filtrar primero solamenmte columnas de interés
    #Formato de hora a 24hrs hh:mm:ss
    df_filtrado['Hora'] = df_filtrado['Hora'].astype(str).str.replace(r'\.', '', regex=True).str.strip() #Limpiar Am, pm
    df_filtrado['Hora'] = pd.to_datetime(df_filtrado['Hora'], errors='coerce') #Forzar solo hora a datatime
    df_filtrado['Hora'] = df_filtrado['Hora'].dt.strftime('%H:%M:%S') #Formatear a 24h
   
    #Obteniendo la fecha para nombrar los archivos de salida
    df_filtrado['Fecha'] = pd.to_datetime(df['Fecha'], format='%y/%m/%d')
    mes = df_filtrado['Fecha'].iloc[0].month
    anio = df_filtrado['Fecha'].iloc[0].year
   
    #Se hacen dos copias, uno compacto y otro extenso
    df_compacto = df_filtrado.copy()
    df_extendido = df_filtrado.copy()
    #Formatea el compacto para legibilidad A y M -> A, Bx -> B, Cx -> C
    df_compacto["Clase"] = df_compacto["Clase"].str.replace(r'^A\d*$', 'A', regex=True)
    df_compacto["Clase"] = df_compacto["Clase"].str.replace(r'^B\d*$', 'B', regex=True)
    df_compacto["Clase"] = df_compacto["Clase"].str.replace(r'^C\d*$', 'C', regex=True)
    df_compacto["Clase"] = df_compacto["Clase"].replace('M', 'A')
    
    return df_compacto, df_extendido, mes, anio
#-----------------------------------------------------------------------------
"""
df = pd.read_excel("13_03_2026.xlsx") #Cambiar por recibir de interfaz

bandera = validandoTabla(df)
if bandera==True:
    df_compacto, df_extenso = formatearDf(df)  
    print(df_compacto)
    print(df_extenso)
    df_compacto.to_excel("pruebaIngresos.xlsx")
    df_extenso.to_excel("pruebaFrecuencias.xlsx")
    #grafica_ingresos = graficaIngresos(df_compacto)
    #grafica_frecuencias = graficaFrecuancias(df_compacto)
    #RETORNAR A LA INTERFAZ
else:
    print("ARCHIVO NO VÁLIDO PARA ANÁLISIS, INGRESAR NUEVO ARCHIVO")  #Cambiar por regresar a la interfaz
"""

