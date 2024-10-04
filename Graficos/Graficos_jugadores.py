# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 08:17:56 2022

@author: luisr
"""




import pandas as pd
import numpy as np
import random
import sys
sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Lesiones")
import aux_func
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

##  Scrapeamos stats de jugadores
season = '2023-2024'
stats = aux_func.scrapping_stats_players_pergame(season,25)

##  Usamos funcion para invertir el nombre
stats = aux_func.invert_name_format(stats)

##  Tenemos que decirle que coja la imagen de cada jugador para cada dato
url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Fotos_jugadores/'

try: 
    nombre = stats['Jugador'].str.split(' ').str[0]
    apellido = stats['Jugador'].str.split(' ').str[1]
    
    stats['url'] = url + nombre.str.lower() + '_' + apellido.str.lower() + '.png'
    
except:
    stats['url'] = url + 'default.png'
    



def plot_stats_player(x_axis,y_axis,num,stats):
    
    
    ##  Hacemos sort con lo que pongamos en el ejeY
    stats2 = stats.sort_values(y_axis,ascending=False)
    
    ##  Convertimos el DF a una version reducida con N elementos
    stats3 = stats2[0:num]
    
    ##  Definimos los datos de los ejes
    x_data = stats3[x_axis]
    y_data = stats3[y_axis]
    
    plt.rcParams["figure.figsize"] = [50, 50]
    plt.rcParams["figure.autolayout"] = True
    
    # def getImage(path):
    #    return OffsetImage(plt.imread(path, format="jpg"), zoom=.1)
    
    def imscatter(x, y, image, ax=None, zoom=1):
        if ax is None:
            ax = plt.gca()
        try:
            image = plt.imread(image,format ='png')
        except TypeError:
            # Likely already an array...
            pass
        im = OffsetImage(image, zoom=zoom)
        x, y = np.atleast_1d(x, y)
        artists = []
        for x0, y0 in zip(x, y):
            ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
            artists.append(ax.add_artist(ab))
        ax.update_datalim(np.column_stack([x, y]))
        ax.autoscale()
        return artists
    
    paths = stats3['url']
    x = np.array(x_data)
    y = np.array(y_data)
    
    with plt.rc_context({ 'axes.edgecolor':'white','xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'black'}):
        fig, ax = plt.subplots()
        for x0, y0, path in zip(x, y, paths):
           try:
               imscatter(x0, y0, path, zoom=0.75, ax=ax)
           except:
               print(path)
               path2 = 'C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Fotos_jugadores/default.png'
               imscatter(x0, y0, path2, zoom=2, ax=ax)
                      
        ax.set_facecolor("black")
        ax.tick_params(axis='both', which='major', labelsize=80)
        ax.tick_params(axis='both', which='major', pad=10)
        ax.xaxis.labelpad = 30
        ax.yaxis.labelpad = 60
        ax.scatter(x, y)
        
        font1 = {'family':'Verdana','color':'white','size':100}
        plt.xlabel(x_axis,fontdict = font1)
        plt.ylabel(y_axis,fontdict = font1)
        
        print(min(x)*0.8)
        # plt.gca().set_xlim(left = min(x) * 0.8)
        # plt.gca().set_xlim(right = max(x) * 1.2)
        # plt.gca().set_ylim(bottom = min(y) * 0.8)
        # plt.gca().set_ylim(bottom = max(y) * 1.2)
        #plt.xlim(min(x)*0.5,max(x)*1.5)
        #plt.ylim(min(y)*0.8,max(y)*1.2)
        
        plt.grid(color = 'white', linestyle = '--', linewidth = 3)
        plt.show()

a = plot_stats_player('MIN', 'PTS',20,stats)

##  PIE CHART: Distribucion de tiros por equipo
##  Scrapeamos stats equipo web
season = '2023-2024'
stast_teams = aux_func.scrapping_stats_teams(season,'No')

##  Para usar las stats de equipo, parseamos nombre de los equipos
stast_teams = aux_func.parse_team_names(stast_teams)


team = 'WAS'

data = stats[(stats['Equipo'] == team) & (stats['MIN'] > 10)]
data = data.sort_values(by = ['FGA'])

data_team = stast_teams[stast_teams['Equipo'] == team]

fga_equipo = float(data_team['FGA'])



labels = data['Jugador']
sizes = data['FGA']/fga_equipo
a = np.ones(len(labels))*0.4
#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels,explode = a, autopct='%1.1f%%')
plt.show()

























