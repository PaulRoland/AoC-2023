# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 06:41:28 2023

@author: Paul
"""
import numpy as np
import time
start_time = time.time_ns()

symbol_map=np.zeros((142,142))
adj_map=np.zeros((142,142))
gear_map=np.zeros((142,142))

number=''
number_list=list()
number_length_list=list()
number_i_list=list()
number_j_list=list()
number_running=0
number_length=0

f = open("input_dag3.txt", "r")
# i vervangen met i+1 voor padding
# j vervangen met j+1 voor padding, scheelt weer min/max gebruiken
for i,line in enumerate(f): 
    for j,letter in enumerate(line):
        if letter.isdigit():
            #bijhouden dat we met een nummer bezig zijn
            number=number+letter
            number_running=1
            number_length=number_length+1
            symbol_map[i+1,j+1]=0
        else:
            if number_running==1:

                number_list.append(number)
                number_length_list.append(number_length)
                number_i_list.append(i+1)
                number_j_list.append(j)
                
                number=''
                number_running=0
                number_length=0  
            
            if(letter != '.' and letter !='\n'):
                symbol_map[i+1,j+1]=1
            if(letter == '*'):
                gear_map[i+1,j+1]=1


#Controleer het symbolen gebied rondom elk nummer en tel op om te zien of het groter gelijk is aan 1
total =0
for index,num in enumerate(number_list):
    #Defineer een gebied rond het nummer. min max gebruikt om rekening te houden met de randen
    i_min = number_i_list[index]-1
    i_max = number_i_list[index]+1
    
    j_min = number_j_list[index]-number_length_list[index]
    j_max = number_j_list[index]+1
    #print(i_min,i_max,j_min,j_max)
    #Tel de symbolmask op om te kijken of het groter is dan 1
    # part 1
    if symbol_map[i_min:i_max+1,j_min:j_max+1].sum()>=1:
        total=total+int(num)

    if gear_map[i_min:i_max+1,j_min:j_max+1].sum()>=1:
        for i in np.arange(i_min,i_max+1,1):
            for j in np.arange(j_min,j_max+1,1):
                adj_map[i,j]=adj_map[i,j]+1 #Houd bij hoevaak we hier langs komen, dit gebruiken we als map. Dit moet 2 zijn. 
                gear_map[i,j]=gear_map[i,j]*int(num) #Schrijf waarde van de adjacent gear in de map


print("Part 1: ",int(total))
print("Part 2: ",int(np.sum(gear_map * (adj_map==2))))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
