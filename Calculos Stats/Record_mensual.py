# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:12:01 2022

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
import calendar

##  Leemos el csv donde tengamos guardada la clasi de la semana pasada
url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Stats/clasi2023-03-03.csv'
last_week = pd.read_csv(url)

##  Scrapeamos los datos actuales
current_week = aux_func.scrapping_clasi()

##  El formato del nombre de equipo es un truño, lo mas sencillo es quedarnos
##  con el nombre del GM, que es siempre la ultima palabra del string
current_week['GM'] = current_week['Equipo'].str.split(' ')
current_week['GM'] = current_week['GM'].apply(lambda x: x[-1])

## Seleccionamos los datos que nos interesan
clasi_final = current_week[['Equipo.1','V','GM']]
clasi_final.columns = ['V', 'D', 'GM']

##  Guardamos csv
clasi_final.to_csv('C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Stats/clasi' + str(datetime.date.today()) + '.csv')

## Hacemos merge para sacar diferencias
total_data = clasi_final.merge(last_week, on='GM',how = 'left')
total_data['V_week'] = total_data['V_x'] - total_data['V_y']
total_data['D_week'] = total_data['D_x'] - total_data['D_y']

data_final = total_data[['GM','V_week','D_week']]

##  Escribimos el mes para el que estamos sacando stats
today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
mes = calendar.month_name[last_month.month]

##  Guardamos record
data_final.to_csv('C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Stats/record_' + mes + '.csv')



















