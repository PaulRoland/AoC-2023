# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 06:08:39 2023

@author: Paul
"""
import numpy as np
import re

def get_maxnumber(number_list):
    res = [eval(i) for i in number_list] #Zet lijst van strings om naar lijst van integers
    return max(res)

games = np.zeros((100,4)) #Container voor alle games: r,g,b,game_id

f = open("input_dag2.txt", "r")
for i,line in enumerate(f):
    #Zoek alle getallen die voor " red", " green" en " blue" komen, neem hiervan max waarde met get_maxnumber. Plaats in container.
    games[i,0]=get_maxnumber(re.findall(r'\d+(?= red)', line))
    games[i,1]=get_maxnumber(re.findall(r'\d+(?= green)', line))
    games[i,2]=get_maxnumber(re.findall(r'\d+(?= blue)', line))
    
    #Game ID
    games[i,3]=get_maxnumber(re.findall(r'(?<=Game )\d+', line)) #Zoek getallen na "Game ", neem max waarde. Game ID zou gewoon oplopend moeten zijn, maargoed
    
f.close()

#Som van alle gameids waar red<=12, green<=13 en blue<=14 Gebruik. r g en b condities als mask op de game ids en optellen maar
max_rgb=[12,13,14]
possible_sum=np.sum(games[:,3]*   (games[:,0]<=max_rgb[0])*(games[:,1]<=max_rgb[1])*(games[:,2]<=max_rgb[2])   )

power_sum=np.sum(games[:,0]*games[:,1]*games[:,2]) #Som van alle r x g x b    

print("Sum of game IDs of possible games: ",int(possible_sum))
print("Sum of Power of all played games:  ",int(power_sum))