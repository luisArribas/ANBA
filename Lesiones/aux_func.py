# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 19:52:57 2022

@author: luisr
"""
##  Llamamos a las librerias para hacer el web scrapping:
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import ttk
import urllib.request
import os
from PIL import Image
from tqdm import tqdm

##  Cargamos la pagina web con las stats de anba
headers = {'User-Agent': 'Firefox'}

def scrapping_stats_players(season,n_pages,flag_playoff,flag_pergame):
    
    print("Scrappeando estadisticas de jugadores. Espere...")

    #####  Bucle recorriendo las paginas de la tabla
    for i in tqdm(range(1,n_pages + 1)):
        
        if flag_playoff == 'Season' and flag_pergame == 'Total':
            url = 'https://anba2k.es/estadisticas/jugadores?season=' + season + '&order=player_name&order_direction=asc&page=' + str(i)+'&mode=totals' 
        elif flag_playoff == 'Season' and flag_pergame == 'Pergame':
            url = 'https://anba2k.es/estadisticas/jugadores?season=' + season + '&order=player_name&order_direction=asc&page=' + str(i)
        elif flag_playoff == 'Playoff' and flag_pergame == 'Total':
            url = 'https://anba2k.es/estadisticas/jugadores?season=' + season + '&order=player_name&order_direction=asc&&phase=playoffs&page=' + str(i)+'&mode=totals'
        elif flag_playoff == 'Playoff' and flag_pergame == 'Pergame':
            url = 'https://anba2k.es/estadisticas/jugadores?season=' + season + '&order=player_name&order_direction=asc&&phase=playoffs&page=' + str(i)

        ##  Descargamos la pagina web con un request
        re = requests.get(url,headers=headers)  
        
        ##  Parseamos el contenido de la web
        soup = BeautifulSoup(re.text, 'lxml') 
        
        ##  Descargamos la tabla
        stats = soup.find_all('table',{'class' : 'players-stats'})
        
        ##  Convertimos la tabla con read_html para que sea mas facil de tratar
        stats2 = pd.read_html(str(stats), decimal=',', thousands='.')
        stats3 = stats2[0]
        if i == 1:
            player_stats = stats3
        else:
            player_stats = pd.concat([player_stats, stats3], ignore_index=True)
            
        ##  Tambien hay que quitar el espacio inicial que algunos tienen
        player_stats['Jugador'] = player_stats['Jugador'].apply(lambda x: x.strip())
        
        ##  Reemplazamos a cancar
        player_stats['Jugador'] = player_stats['Jugador'].replace('Vlatko o Čančar','Vlatko Čančar') 
            
    return player_stats

def scrapping_stats_teams(season,flag_playoff):
    
    print("Scrappeando estadisticas de equipos. Espere...")
    
    if flag_playoff == 'Playoff':
        url = 'https://anba2k.es/estadisticas/equipos?season=' + season + '&order=PER_W&order_direction=desc&phase=playoffs' 
    elif flag_playoff == 'Season':
        url = 'https://anba2k.es/estadisticas/equipos?season=' + season + '&order=PER_W&order_direction=desc'
    

    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)  

    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 

    ##  Descargamos la tabla
    team_stats = soup.find_all('table',{'class' : 'players-stats'})

    ##  Convertimos la tabla con read_html para que sea mas facil de tratar
    team_stats2 = pd.read_html(str(team_stats), decimal=',', thousands='.')
    team_stats3 = team_stats2[0]
    
    return team_stats3

def scrapping_player_index(n_pages):
    
    print("Scrappeando indice de jugadores. Espere...")
    
    ##  Indice de jugadores -> Para tener todos los jugadores, no solo los que 
    ##  hayan jugado algun minuto
    for i in tqdm(range(1,n_pages + 1)):
        
        url = 'https://anba2k.es/jugadores?page=' + str(i) 
        
        ##  Descargamos la pagina web con un request
        re = requests.get(url,headers=headers)  
        
        ##  Parseamos el contenido de la web
        #soup = BeautifulSoup( re.text, 'html.parser')
        soup = BeautifulSoup(re.text, 'lxml') 
        
        ##  Descargamos la tabla
        index = soup.find_all('table',{'class' : 'w-full'})
        
        ##  Convertimos la tabla con read_html para que sea mas facil de tratar
        index2 = pd.read_html(str(index), decimal=',', thousands='.')
        index3 = index2[0]
        if i == 1:
            full_index = index3
        else:
            full_index = pd.concat([full_index, index3], ignore_index=True)

    return full_index

def invert_name_format(stats_players,nombre_col):
    
    nombre = [i.split(', ') for i in stats_players[nombre_col]]

    nombre_inv = [name[1] + ' ' + name[0] for name in nombre]
    stats_players[nombre_col] = nombre_inv
    
    return stats_players
    
    
    
    
def parse_team_names(stats_teams):
    
    stats_teams = stats_teams.replace('Atlanta Hawks','ATL')
    stats_teams = stats_teams.replace('Boston Celtics','BOS')
    stats_teams = stats_teams.replace('Charlotte Hornets','CHA')
    stats_teams = stats_teams.replace('Chicago Bulls','CHI')
    stats_teams = stats_teams.replace('Cleveland Cavaliers','CLE')
    stats_teams = stats_teams.replace('Dallas Mavericks','DAL')
    stats_teams = stats_teams.replace('Detroit Pistons','DET')
    stats_teams = stats_teams.replace('Denver Nuggets','DEN')
    stats_teams = stats_teams.replace('Golden State Warriors','GSW')
    stats_teams = stats_teams.replace('Houston Rockets','HOU')
    stats_teams = stats_teams.replace('Indiana Pacers','IND')
    stats_teams = stats_teams.replace('Los Angeles Lakers','LAL')
    stats_teams = stats_teams.replace('Los Angeles Clippers','LAC')
    stats_teams = stats_teams.replace('Milwaukee Bucks','MIL')
    stats_teams = stats_teams.replace('Minnesota Timberwolves','MIN')
    stats_teams = stats_teams.replace('Orlando Magic','ORL')
    stats_teams = stats_teams.replace('Philadelphia 76ers','PHI')
    stats_teams = stats_teams.replace('Phoenix Suns','PHO')
    stats_teams = stats_teams.replace('Brooklyn Nets','BKN')
    stats_teams = stats_teams.replace('Miami Heat','MIA')
    stats_teams = stats_teams.replace('Sacramento Kings','SAC')
    stats_teams = stats_teams.replace('Oklahoma City Thunder','OKC')
    stats_teams = stats_teams.replace('San Antonio Spurs','SAS')
    stats_teams = stats_teams.replace('Portland Trail Blazers','POR')
    stats_teams = stats_teams.replace('Toronto Raptors','TOR')
    stats_teams = stats_teams.replace('Utah Jazz','UTA')
    stats_teams = stats_teams.replace('Memphis Grizzlies','MEM')
    stats_teams = stats_teams.replace('New York Knicks','NYK')
    stats_teams = stats_teams.replace('New Orleans Pelicans','NOP')
    stats_teams = stats_teams.replace('Washington Wizards','WAS')
    
    return stats_teams
    
def popupmsg(msg): 
     
    popup = tk.Tk()
    popup.wm_title("!")
    NORM_FONT= ("Verdana", 10)
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
   
def scrapping_lesionados():
    
    ##  Stats Equipo -> Para saber el numero de partidos de cada equipo
    url = 'https://anba2k.es/jugadores/lesionados'

    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)  

    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 

    ##  Descargamos la tabla
    lesionados = soup.find_all('table',{'class' : 'w-full'})

    ##  Convertimos la tabla con read_html para que sea mas facil de tratar
    lesionados = pd.read_html(str(lesionados), decimal=',', thousands='.')
    lesionados = lesionados[0]
    
    lesionados.to_csv('C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones/lesionados.csv')
    
    return lesionados
    
def scrapping_clasi():
    
    ##  Stats Equipo -> Para saber el numero de partidos de cada equipo
    url = 'https://anba2k.es/clasificaciones?season=2022-2023&view=general' 

    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)  

    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 

    ##  Descargamos la tabla
    clasi = soup.find_all('table',{'class' : 'w-full'})

    ##  Convertimos la tabla con read_html para que sea mas facil de tratar
    clasi = pd.read_html(str(clasi), decimal=',', thousands='.')
    clasi = clasi[0]
    
    return clasi    
    
    
def scrapping_BR_Teams(flag_playoff):
    
    if flag_playoff == 'Playoff':
        url = 'https://www.basketball-reference.com/playoffs/NBA_2024.html'
    elif flag_playoff == 'Season':
        url = 'https://www.basketball-reference.com/leagues/NBA_2024.html'
    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)  

    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 

    ##  Descargamos la tabla
    stats = soup.find_all('table',{'id' : 'per_game-team'})

    ##  Convertimos la tabla con read_html para que sea mas facil de tratar
    stats = pd.read_html(str(stats))
    stats = stats[0]
    
    url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Stats/teams_BR.csv'
    stats.to_csv(url)    
    return stats

def download_image(url, file_path, file_name):
    full_path = file_path + file_name
    urllib.request.urlretrieve(url, full_path)    

def download_player_images():
    ##  Indice de jugadores 
    path = 'C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Fotos_jugadores/'
    for i in range(1,64 + 1):
        print(i)
        url = 'https://anba2k.es/jugadores?page=' + str(i) 
        
        ##  Descargamos la pagina web con un request
        re = requests.get(url,headers=headers)  
        
        ##  Parseamos el contenido de la web
        #soup = BeautifulSoup( re.text, 'html.parser')
        soup = BeautifulSoup(re.text, 'lxml') 
        
        ##  Descargamos la tabla
        index = soup.find_all('img')
        
        for item in index:
            src = item['src']
            print(src)
            
            try:
                name = src.split('players/')[1]
                print(name)
                download_image(src,path,name)
            except:
                print('no es imagen de jugador')
                
                
def reescalar_img():

    path = 'C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Fotos_jugadores/'                
     
    for filename in os.listdir(path):
        print(filename)
        f = os.path.join(path, filename)
        
        img = Image.open(f)
        img = img.resize((400,400),Image.ANTIALIAS)
        img.save(f)
        
def scrapping_ratings(player_name):

    url = 'https://hoopshype.com/player/' + str(player_name) +  '/2k/'
    
    ##  Descargamos la pagina web con un request
    re = requests.get(url,headers=headers)
    
    ##  Parseamos el contenido de la web
    soup = BeautifulSoup(re.text, 'lxml') 
    
    # print('Classes of each table:')
    # for table in soup.find_all('div'):
    #     print(table.get('class'))
        
    table = soup.find('div', class_= 'player-payroll')
    
    ratings = soup.find_all('td',{'class' : 'table-value2'})    
    
    ##  Convertimos la tabla con read_html para que sea mas facil de tratar
    ratings2 = pd.read_html(str(table))
    ratings3 = ratings2[0]
    
    ##  Añadimos nombre
    ratings3['Name'] = player_name
    
    ratings3 = ratings3[['Name','Season','Team','Rating']]
    
    return ratings3


 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    