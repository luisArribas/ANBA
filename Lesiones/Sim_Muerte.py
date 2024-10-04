# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 11:34:39 2022

@author: luisr
"""




def preparacion_datos(equipos_vivos):

    ##  Llamamos a las librerias para hacer el web scrapping
    import pandas as pd
    import numpy as np
    import random
    import sys
    sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones")
    import aux_func
    
    ##  Definimos de que temporada queremos los datos
    season = '2023-2024'
    
    ##  Scrapeamos stats jugadores
    stats_players = aux_func.scrapping_stats_players(season, 27)
    
    ##  Stats Equipo -> Para saber el numero de partidos de cada equipo
    stats_teams = aux_func.scrapping_stats_teams(season,'No')
    
    ##  Indice de jugadores
    index = aux_func.scrapping_player_index(71)
    index = index.replace("PHX","PHO")
    
    ##  Cogemos los que tienen equipo actualmente
    index = index[index['Equipo'] != 'Agente Libre']        
          
    ##  Para poder hacer merge necesitamos que los nombres esten en el mismo format
    stats_players = aux_func.invert_name_format(stats_players)
    
    ##  Tambien hay que quitar el espacio inicial que algunos tienen
    stats_players['Jugador'] = stats_players['Jugador'].apply(lambda x: x.strip())
    
    ##  Reemplazamos a cancar
    stats_players['Jugador'] = stats_players['Jugador'].replace('Vlatko o Čančar','Vlatko Čančar') 
    
    ## Merge
    merged_stats = index.merge(stats_players, on = 'Jugador',how = 'right')
    
    ###########################################################################
    ##  Aqui saldran varios que tienen stats y no estan en el index. Por ahora hay que corregirlo a mano
    no_stats = merged_stats[merged_stats['Peso'].isna()]
    
    ##  Seleccionamos solo las columnas que vamos a usar
    final_stats = merged_stats[['Jugador','Equipo_x','PJ','MIN']]
    
    ##  Reemplazamos NAs por 0
    final_stats['MIN'] = final_stats['MIN'].replace(np.nan, 0)
    final_stats['PJ'] = final_stats['PJ'].replace(np.nan, 0)
    
    ##  Para usar las stats de equipo, parseamos nombre de los equipos
    stats_teams = aux_func.parse_team_names(stats_teams)
    
    ##  Nos falta otro merge para los partidos jugados por el equipo
    merged_stats2 = final_stats.merge(stats_teams, left_on='Equipo_x', right_on='Equipo',how = 'left')
    
    ##  Ya tenemos el dataframe final
    final_stats = merged_stats2[['Jugador','Equipo_x','PJ_x','MIN','PJ_y']]
    final_stats.columns =['Jugador','Equipo','PJ_jug','MIN','PJ_Eq']
    
    ##  Calculamos los pesos de cada jugador segun sus minutos
    final_stats['peso'] = (final_stats['MIN'] + final_stats['PJ_Eq'] * 10)
    
    ##  Filtramos solo para los equipos vivos
    final_stats = final_stats[final_stats['Equipo'].isin(equipos_vivos)]
    
    return final_stats

def Generar_Muerte(final_stats):
    
    import pandas as pd
    import numpy as np
    import random
    import sys
    sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Lesiones")
    import aux_func
    
    dead_player = random.choices(list(final_stats['Jugador']), weights=tuple(final_stats['peso']), k=1)
    
    ## Si toca lesion, hay que elegir cual y la duracion
    
    ## Creamos dataframe con los datos de las lesiones
    lesiones = ['Quadriceps tendon','ACL','MCL','Achilles','Patellar tendon']
    
    datos_lesiones = pd.DataFrame(lesiones)
    datos_lesiones['numero'] = [3,33,5,23,6]
    datos_lesiones['media'] = [305,410,434,346,413]
    datos_lesiones['min'] = [212,232,194,210,198]
    datos_lesiones['max'] = [371,1110,836,614,886]
    datos_lesiones['stdev'] = [83,179,251,99,246]
    
    ##  Elegimos lesion aleatoriamente usando las prob de ocurrencia
    lesion = random.choices(list(datos_lesiones[0]), weights=tuple(datos_lesiones['numero']), k=1)
    lesion = lesion[0]
    ##  Para la duracion, debemos sacar un num aletorio con distrib normal centrada
    ##  en la media calculada
    
    mean = datos_lesiones[datos_lesiones[0] == lesion]['media']
    stdev = datos_lesiones[datos_lesiones[0] == lesion]['stdev']
    minimo = float(datos_lesiones[datos_lesiones[0] == lesion]['min']) 
    maximo = float(datos_lesiones[datos_lesiones[0] == lesion]['max'])
    
    duracion = float(random.gauss(mean, stdev))
    while duracion < minimo or duracion > maximo:
        duracion = float(random.gauss(mean, stdev))
    
    duracion = round(duracion,0)
    
    aux_func.popupmsg('Jugador: ' + str(dead_player[0]) + '  lesion: ' + str(lesion) + '    duracion: ' + str(duracion) + ' dias')






















