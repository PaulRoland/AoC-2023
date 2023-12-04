# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 06:01:33 2023

@author: Paul
"""
import time
start_time = time.time()


import numpy as np
import re

def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

def number_of_matches(list1,list2): 
    matches=0
    for item in list1:
        if item in list2:
            matches = matches+1
            continue
    return matches


total_matchpoints =0
copies_list = np.ones((207,1)) #one of each card

f = open("input_dag4.txt", "r")
for i,line in enumerate(f):
    numbers_found = re.findall(r'\d+',line) #Lijst van nummers
    number_list=get_number_list(numbers_found)
    
    matches=number_of_matches(number_list[1:11],number_list[11:]) #Mischien sneller om een functie te maken die op dubbele waardes controleert, scheelt weer opsplitsen
        
    if matches >= 1:
        total_matchpoints = total_matchpoints +  2**(matches-1)
        
    #create copies of the next n-cards (#matches) equal to the amount this card has been won
    copies_list[i+1:i+matches+1]=copies_list[i+1:i+matches+1]+copies_list[i]
    
f.close()
print(total_matchpoints)
print(int(np.sum(copies_list)))
print("--- %s seconds ---" % (time.time() - start_time))
print('22488,7013204')