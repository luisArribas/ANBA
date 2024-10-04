# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 22:42:11 2022

@author: luisr
"""



import pandas as pd
import numpy as np
import random
import sys
sys.path.append("C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Lesiones")
import aux_func
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

##  Scrapeamos stats equipo web
season = '2023-2024'
playoffs = 'No'
stats = aux_func.scrapping_stats_teams(season,playoffs)

##  Para usar las stats de equipo, parseamos nombre de los equipos
stats = aux_func.parse_team_names(stats)


stats.loc['media'] = stats.mean()
stats['Equipo'] = stats['Equipo'].fillna('ANBA')

##  Para meter la media NBA, scrappeamos datos o los leemos de csv
url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/23_24/Stats/teams_BR.csv'
stats_nba = aux_func.scrapping_BR_Teams(playoffs)
#stats_nba = pd.read_csv(url)

##  Añadimos al DF de ANBA los datos medios de NBA
stats_nba.columns = ['RK','Equipo','PJ','MP','FGM','FGA','FG%','3PM','3PA',
                     '3P%','2P','2PA','2P%','TLM','TLA','TL%','R.O','R.D',
                     'REB','AST','ROB','TAP','PER','FP','PTS']

stats_nba.at[len(stats_nba)-1,'FG%'] = stats_nba['FGM'].sum()/stats_nba['FGA'].sum()*100
stats_nba.at[len(stats_nba)-1,'3P%'] = stats_nba['3PM'].sum()/stats_nba['3PA'].sum()*100
stats_nba.at[len(stats_nba)-1,'TL%']= stats_nba['TLM'].sum()/stats_nba['TLA'].sum()*100

stats.loc[32] = stats_nba.iloc[-1]
stats.at[32,'Equipo']='NBA'

##  Tenemos que decirle que coja el logo de cada equipo para cada dato
url = 'C:/Users/luisr/OneDrive/Desktop/ANBA/22_23/Logos/'
stats['url'] = url + stats['Equipo'] + '.png'
    
    
def plot_stats_teams(x_axis,y_axis):
    
    ##  Definimos los datos de los ejes
    x_data = stats[x_axis]
    y_data = stats[y_axis]
    
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
    
    paths = stats['url']
    x = np.array(x_data)
    y = np.array(y_data)
    
    with plt.rc_context({ 'axes.edgecolor':'white','xtick.color':'white', 'ytick.color':'white', 'figure.facecolor':'black'}):
        fig, ax = plt.subplots()
        for x0, y0, path in zip(x, y, paths):
           if 'ANBA.png' in path:
               imscatter(x0, y0, path, zoom=0.75, ax=ax)
           elif 'OKC.png' in path:
                   imscatter(x0, y0, path, zoom=1.2, ax=ax)
           elif 'NOP.png' in path:
               imscatter(x0, y0, path, zoom=1.8, ax=ax)
           elif 'SAS.png' in path:
               imscatter(x0, y0, path, zoom=1.3, ax=ax)
           elif 'MIA.png' in path:
               imscatter(x0, y0, path, zoom=1.4, ax=ax)
           elif 'BOS.png' in path:
               imscatter(x0, y0, path, zoom=1.2, ax=ax)
           elif 'UTA.png' in path:
               imscatter(x0, y0, path, zoom=1.3, ax=ax)
           elif 'ORL.png' in path:
               imscatter(x0, y0, path, zoom=0.8, ax=ax)
                   
           else:
               imscatter(x0, y0, path, zoom=1, ax=ax)
        ax.set_facecolor("black")
        ax.tick_params(axis='both', which='major', labelsize=80)
        ax.tick_params(axis='both', which='major', pad=10)
        ax.xaxis.labelpad = 30
        ax.yaxis.labelpad = 60
        ax.scatter(x, y)
        
        font1 = {'family':'Verdana','color':'white','size':100}
        plt.xlabel(x_axis,fontdict = font1)
        plt.ylabel(y_axis,fontdict = font1)
        
        plt.grid(color = 'white', linestyle = '--', linewidth = 3)
        plt.show()

a = plot_stats_teams('3PA', '3PM')
















