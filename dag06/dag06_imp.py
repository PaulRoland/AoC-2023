# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 06:28:45 2023

@author: Paul
"""
import time
start_time = time.time_ns()

import math
def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst

def get_number_list2(lst):
    total=''
    for item in lst:
        total=total+item
    return int(total)

def ways_to_win(distance,time): 
    wrtl=math.sqrt(time*time-4*distance)
    t1 = math.floor(0.5*(time-wrtl))
    t2 = math.ceil(0.5*(time+wrtl))
    return t2-t1-1


f = open("input_dag6.txt", "r")
for i,line in enumerate(f):
    if(i==0):
        time_list = get_number_list(line.split()[1:])
        time_total= get_number_list2(line.split()[1:])
    if(i==1):
        distance_list = get_number_list(line.split()[1:])
        distance_total= get_number_list2(line.split()[1:])
f.close()

multiplicity=1
for distance,times in zip(distance_list,time_list):    
    multiplicity = multiplicity*ways_to_win(distance,times)
    
print("Dag 6, Part 1:",multiplicity)
print("Dag 6, Part 2:",ways_to_win(distance_total,time_total))

print("--- %s ms ---" % ((time.time_ns()- start_time)/1000000))
