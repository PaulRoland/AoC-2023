# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 06:08:39 2023

@author: Paul
"""

f = open("input_dag2.txt", "r")
import numpy as np
import re

game_combination = np.zeros((100,5)) #id,r,g,b,power

def get_number(text):
    if text:
        return int(re.findall(r'\d+',text[0])[0])
    return 0

i=0
for line in f:
    game_entries=line.split(';')
    #get game id van eerste stukje regel. Waarschijnlijk lopen ze gewoon netjes op
    #game_combination[i,0]=int(re.findall(r'\d+', game_entries[0].split(":")[0])[0])
    game_combination[i,0]=i+1
  
    #Bekijk alle gameentries, onthoud het maximum aantal r g en b ballen
    for game in game_entries:
        
        red_found=get_number(re.findall(r'\d+ red', game))
        green_found=get_number(re.findall(r'\d+ green', game))
        blue_found=get_number(re.findall(r'\d+ blue', game))

        #Neem de grootste rgb waarde over in de game_combination tabel
        game_combination[i,1]=np.max([game_combination[i,1],red_found])
        game_combination[i,2]=np.max([game_combination[i,2],green_found])
        game_combination[i,3]=np.max([game_combination[i,3],blue_found])
    
    #Bereken de power van een spel: r*g*b
    game_combination[i,4]=game_combination[i,1] * game_combination[i,2] * game_combination[i,3]
    i=i+1
    
f.close()


#We hebben nu een lijst met het hoogste getal r,g,b per game met game id en de power
possible_sum=0
power_sum=0

for row in game_combination:
    #12 red, 13 green, 14 blue
    power_sum=power_sum+row[4]
    if row[1]<12+1 and row[2]<13+1 and row[3]<14+1:
        possible_sum=possible_sum+row[0]
        print(row[1],row[2],row[3],"Possible!")
    else:
        print(row[1],row[2],row[3],"No! This is impossible!")
        
print("Possible sum",possible_sum)
print("Power sum",power_sum)
