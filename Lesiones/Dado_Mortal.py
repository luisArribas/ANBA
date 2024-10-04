# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 18:31:28 2023

@author: luisr
"""

##  Script para simular las lesiones con duracion > 1 año

##  REGLAS
##      Season: 
##          - 1 lanzamiento por semana, con la prob = n_lesiones /n_semanas
##          - La prob de que le toque a un jugador viene definida en el codigo
##          - Jugadores lesionados estan excuidos
##      Playoff:
##          - Lanzamiento diario con prob = prob_semana /7
##          - En cada momento se aplicará solo a jugadores de equipos en activo


def lanzamos_dado_mortal():

    ##  Importamos librerias
    import numpy as np
    import pandas as pd
    import sys
    sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones")
    import aux_func
    import Sim_Muerte
    
    ## 1. Decidimos si hay muerte.
    
    ##  Toda la liga
    #equipos_vivos = ['ATL','BOS','BKN','CHI','CHA','CLE','DET','IND','MIA','MIL','NYK','ORL','PHI','TOR','WAS','DAL','DEN','GSW','HOU','LAC','LAL','MEM','MIN','NOP','OKC','PHO','POR','SAC','SAS','UTA']
    
    ##  Vamos actualizando cada dia los que quedan vivos
    equipos_vivos = ['ATL','BOS','CHA','MIL','NYK','ORL','PHI','TOR','WAS','DAL','DEN','HOU','LAC','LAL','MIN','OKC','PHO','POR']

    ##  Season
    prob_semana = 0.206

    ##  PO
    prob_semana = (0.206/7) * (len(equipos_vivos)/30)
    
    ##  Playoffs
    #prob_diaria = prob_semana/7
    
    ##  Lanzamos dado
    dado_muerte = np.random.choice(np.arange(0, 2), p=[1-prob_semana, prob_semana])
    
    ##  2. Si sale que no hay muerte, paramos ejecucion
    if (dado_muerte == 0):
        aux_func.popupmsg('No hay muertes hoy.')
        
    ##  3. Si hay muerte llamamos a la funcion para elegir agraciado
    if (dado_muerte == 1):
        aux_func.popupmsg('FATALITY!! Calculando agraciado.')
        
        datos = Sim_Muerte.preparacion_datos(equipos_vivos)
        Sim_Muerte.Generar_Muerte(datos)
