# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 18:52:35 2022

@author: luisr
"""

##  Llamamos a las librerias para hacer el web scrapping
import pandas as pd
import numpy as np
import random
import sys
sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones")
import aux_func
import datetime


##  Definimos de que temporada queremos los datos
season = '2023-2024'

##  Scrapeamos stats jugadores
stats_players = aux_func.scrapping_stats_players(season, 23)

stats_players.to_csv('C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Stats/stats_players' + str(datetime.date.today()) + '.csv')


##  Cargamos las stats del periodo anterior
##  Leemos el csv donde tengamos guardada la clasi de la semana pasada
url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Stats/stats_players2023-03-04.csv'
last_stats = pd.read_csv(url)

##  Hacemos merge para tener ambos conjuntos en un mismo DF
merged_stats = stats_players.merge(last_stats, on='Jugador',how = 'left')

##  Creamos el DF con los promedios del mes
##  Seleccionamos solo las columnas que vamos a usar
merged_stats = merged_stats[['Jugador','Equipo_x','PJ_x','MIN_x','PTS_x','FGM_x','FGA_x','3PM_x','3PA_x','TLM_x','TLA_x','REB_x','AST_x','ROB_x','PER_x','TAP_x',
                             'PJ_y','MIN_y','PTS_y','FGM_y','FGA_y','3PM_y','3PA_y','TLM_y','TLA_y','REB_y','AST_y','ROB_y','PER_y','TAP_y']]


monthly_stats = merged_stats
monthly_stats = monthly_stats.replace(np.nan, 0)

monthly_stats['PJ'] = monthly_stats['PJ_x'] - monthly_stats['PJ_y']
monthly_stats['MIN'] = (monthly_stats['MIN_x'] - monthly_stats['MIN_y'])/monthly_stats['PJ']
monthly_stats['PTS'] = (monthly_stats['PTS_x'] - monthly_stats['PTS_y'])/monthly_stats['PJ']
monthly_stats['REB'] = (monthly_stats['REB_x'] - monthly_stats['REB_y'])/monthly_stats['PJ']
monthly_stats['AST'] = (monthly_stats['AST_x'] - monthly_stats['AST_y'])/monthly_stats['PJ']
monthly_stats['ROB'] = (monthly_stats['ROB_x'] - monthly_stats['ROB_y'])/monthly_stats['PJ']
monthly_stats['TAP'] = (monthly_stats['TAP_x'] - monthly_stats['TAP_y'])/monthly_stats['PJ']
monthly_stats['FGM'] = (monthly_stats['FGM_x'] - monthly_stats['FGM_y'])/monthly_stats['PJ']
monthly_stats['FGA'] = (monthly_stats['FGA_x'] - monthly_stats['FGA_y'])/monthly_stats['PJ']
monthly_stats['3PM'] = (monthly_stats['3PM_x'] - monthly_stats['3PM_y'])/monthly_stats['PJ']
monthly_stats['3PA'] = (monthly_stats['3PA_x'] - monthly_stats['3PA_y'])/monthly_stats['PJ']
monthly_stats['TLA'] = (monthly_stats['TLA_x'] - monthly_stats['TLA_y'])/monthly_stats['PJ']
monthly_stats['TLM'] = (monthly_stats['TLM_x'] - monthly_stats['TLM_y'])/monthly_stats['PJ']
monthly_stats['FG%'] = monthly_stats['FGM']/monthly_stats['FGA']
monthly_stats['3P%'] = monthly_stats['3PM']/monthly_stats['3PA']
monthly_stats['TL%'] = monthly_stats['TLM']/monthly_stats['TLA']

monthly_stats = monthly_stats[['Jugador','Equipo_x','PJ','MIN','PTS','REB','AST','ROB','TAP','FGM','FGA','FG%','3PM','3PA','3P%','TLM','TLA','TL%']]

monthly_stats = monthly_stats.replace(np.nan, 0)
## Exportamos
import datetime
import calendar
today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
mes = calendar.month_name[last_month.month]
monthly_stats.to_csv('C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Stats/stats' + mes + '.csv')






