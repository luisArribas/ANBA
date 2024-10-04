# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 21:50:52 2024

@author: luisr
"""

##  Llamamos a las librerias
import pandas as pd
import numpy as np


##  Tomamos como ejemplo el trade de Mikal Bridges. Necesitamos recopilar todas las cifras

salarios_equipo_A = [28170815,1119563]
salarios_equipo_B = [10489600,10489600,8882638]

excepciones_equipo_A = [12707040,7277000]
excepciones_equipo_B = [1543955,10932818]

payroll_equipo_A = 166357589 +  28170815 + 1119563 - 10489600 - 10489600 - 8882638
payroll_equipo_A = 162954060 -  28170815 - 1119563 + 10489600 + 10489600 + 8882638

apron = 172346000

##  Construimos la calculadora de trades
sum(salarios_equipo_A)
