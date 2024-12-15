# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 06:28:45 2023

@author: Paul
"""

def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

def get_number_list2(lst):
    total=''
    for item in lst:
        total=total+item
    return int(total)

def way_to_wins(distance,time):
    wins=0
    for time_held in range(time):
        if time_held*(time-time_held)>distance:
            #print("Traveled",time_held*(time-time_held),distance)
            wins=wins+1
    return wins


f = open("input_dag6.txt", "r")
for i,line in enumerate(f):
    if(i==0):
        time_list = get_number_list(line.split()[1:])
    if(i==1):
        distance_list = get_number_list(line.split()[1:])
f.close()

multiplicity=1
for i,distance in enumerate(distance_list):    
    multiplicity = multiplicity*way_to_wins(distance,time_list[i])

print(multiplicity)


f = open("input_dag6.txt", "r")
for i,line in enumerate(f):
    if(i==0):
        time_list = get_number_list2((line.split()[1:]))
    if(i==1):
        distance_list = get_number_list2((line.split()[1:]))
f.close()

multiplicity=1
multiplicity = multiplicity*way_to_wins(distance_list,time_list)

print(multiplicity)
