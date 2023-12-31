# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 06:41:28 2023

@author: Paul
"""
import numpy as np
import time
start_time = time.time()

symbol_map=np.zeros((140,140))

number=''
number_list=list()
number_length_list=list()
number_i_list=list()
number_j_list=list()
number_running=0
number_length=0

f = open("input_dag3.txt", "r")
for i,line in enumerate(f):

 
    for j,letter in enumerate(line):
        if letter.isdigit():
            #bijhouden dat we met een nummer bezig zijn
            number=number+letter
            number_running=1
            number_length=number_length+1
            symbol_map[i,j]=0
        else:
            if number_running==1:

                number_list.append(number)
                number_length_list.append(number_length)
                number_i_list.append(i)
                number_j_list.append(j-1)
                
                number=''
                number_running=0
                number_length=0  
                
            if(letter != '.'):
                if(j<140):
                   symbol_map[i,j]=1


#Zoek de locatie en lengte van elk getal.
#Controleer het symbolen gebied rondom dit nummer en tel op om te zien of het groter gelijk is aan 1
total =0
for index,num in enumerate(number_list):
    #Defineer een gebied rond het nummer. min max om rekening te houden met de randen
    i_min = np.max([0,number_i_list[index]-1])
    i_max = np.min([139,number_i_list[index]+1])
    
    j_min = np.max([0,number_j_list[index]-number_length_list[index]])
    j_max = np.min([139,number_j_list[index]+1])
    #print(i_min,i_max,j_min,j_max)
    #Tel de symbolmask op om te kijken of het groter is dan 1
    if np.sum(symbol_map[i_min:i_max+1,j_min:j_max+1]) >= 1:
        total=total+int(num)
        #print(num,"has no adjacancy")
print(int(total))
print("--- %s seconds ---" % (time.time() - start_time))
