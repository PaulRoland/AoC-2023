# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:01:33 2023

@author: Paul
"""
import time
start_time = time.time()

import numpy as np
import re

total_matchpoints =0
copies_list = np.ones((207,1)) #one of each card
matchpoints=[0,1,2,4,8,16,32,64,128,256,512]
f = open("input_dag4.txt", "r")
for i,line in enumerate(f):
    numbers_found = re.findall(r'\d+',line)[1:] #Lijst van nummers, maar niet het kaart nummer
    matches=35-len(set(numbers_found)) #Set heeft alleen de unieke items van de list, het lengteverschil is dus het aantal matches
    total_matchpoints = total_matchpoints +  matchpoints[matches] #uit een lijst halen van de punten scheelde 0.5s op 10.000 runs tov if statement en berekening
    copies_list[i+1:i+matches+1]=copies_list[i+1:i+matches+1]+copies_list[i] #create copies of the next n-cards (#matches) equal to the amount the current card has been won
f.close()
print("Part one:", total_matchpoints)
print("Part two:", int(np.sum(copies_list)))   
print("--- %s seconds ---" % (time.time() - start_time))
