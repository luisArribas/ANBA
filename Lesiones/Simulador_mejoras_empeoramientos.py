# -*- coding: utf-8 -*-
"""
Created on Sun Apr  9 14:42:32 2023

@author: luisr
"""

##  Script para simular las mejoras y empeoramientos semanales/diarios

##  REGLAS
##      Season: 
##          - 1 mejora y 1 empeoramiento por semana
##          - Un jugador que ya ha mejorado/empeorado se descarta en proximas
##          - Lesiones de temporada (+180) entran una vez al sorteo y no mas.
##      Playoff:
##          - Dados independientes mejora/empeoramiento
##          - 2 de cada por semana
##          - Dado diario con probabilidad 2/7
##          - Tiene en cuenta todo el listado de lesionados.


def lanzamos_dados():

    ##  Importamos librerias
    import numpy as np
    import pandas as pd
    import sys
    sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Lesiones")
    import aux_func
    
    
    ## 1. Decidimos si hay mejora/empeoramiento.
    
    ##  Season
    prob = 1
    
    ##  Playoffs
    #prob = 2/7
    
    ##  Lanzamos dados
    dado_mejora = np.random.choice(np.arange(0, 2), p=[1-prob, prob])
    dado_empeoramiento = np.random.choice(np.arange(0, 2), p=[1-prob, prob])
    
    ##  Si en playoffs ya se ha cubierto el cupo semanal o al reves, tenemos que forzarlo
    ##  En temporada ambos valen 1
    dado_mejora = 1
    dado_empeoramiento = 1
    
    ##  2. Si en ambos dados sale que no hay cambios, paramos ejecucion
    if (dado_mejora == 0) & (dado_empeoramiento == 0):
        aux_func.popupmsg('No hay mejoras ni empeoramientos hoy.')
        
    ##  3. Si hay mejoras/empeoramientos, lo primero es descargar la lista de 
    ##  jugadores lesionados de la web y la lista de descartados
    
    ##  Lesionados
    lesionados_web = aux_func.scrapping_lesionados()
    
    ##  Descartados
    path = 'C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones/Descartados.csv'
    descartados = pd.read_csv(path,header = None)
    descartados.columns = ['Mojon','Jugador']
    descartados = descartados[['Jugador']]
    
    ##  4. Si un jugador está en descartados pero no en lesionados, significa que 
    ##  ya se recuperó. Hay que quitarlo de descartados
    descartados = descartados.merge(lesionados_web['Jugador'],how = 'inner')
    
    ##  5. A la lista de lesionados le quitamos los descartados
    lesionados = lesionados_web[~lesionados_web['Jugador'].isin(descartados['Jugador'])]
    
    ##  6. Si hay mejora, elegimos el jugador a mejorar y la cantidad de partidos
    if (dado_mejora == 1):
        jugador_mejora = np.random.choice(lesionados['Jugador'])
        datos_jug = lesionados[lesionados['Jugador'] == jugador_mejora]
        n_part_original = datos_jug['Partidos']
        modif = np.random.choice(np.arange(20, 90))/100
        n_part_mod = int(np.round(n_part_original * modif))
        aux_func.popupmsg('La lesion de ' + jugador_mejora + ' mejora y pasa a ' + str(n_part_mod) + ' partidos.')
        aux = pd.DataFrame([jugador_mejora],columns=['Jugador'])
        descartados = descartados.append(aux)
        
    ##  7. Idem con el empeoramiento
    if (dado_empeoramiento == 1):
        jugador_empeora = np.random.choice(lesionados['Jugador'])
        datos_jug = lesionados[lesionados['Jugador'] == jugador_empeora]
        n_part_original = datos_jug['Partidos']
        modif = np.random.choice(np.arange(20, 90))/100
        n_part_mod = int(np.round(n_part_original * (1 + modif)))
        aux_func.popupmsg('La lesion de ' + jugador_empeora + ' empeora y pasa a ' + str(n_part_mod) + ' partidos.')
        aux2 = pd.DataFrame([jugador_empeora],columns=['Jugador'])
        descartados = descartados.append(aux2)
        
    ##  8. Actualizamos lista de descartados
    descartados.to_csv(path)
     