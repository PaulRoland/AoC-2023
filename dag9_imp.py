# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 05:59:00 2023

@author: Paul
"""

import time
start_time = time.time_ns()

import numpy as np

def get_number_list(lst):
    new_lst = [int(x) for x in lst]
    return new_lst


def get_difference(int_list):
    diff_list=int_list[1:]-int_list[:-1]
    if set(diff_list)=={0}:
        return [0,0]
    else:
        return_list = get_difference(diff_list) 
        return [diff_list[0]-return_list[0],diff_list[-1]+return_list[-1]]             

f = open("input_dag9.txt", "r")
totalsum1=0
totalsum2=0
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','')
    numbers=np.array(get_number_list(line.split()))
    
    diff_lr=get_difference(numbers)
    totalsum1=totalsum1+numbers[-1]+diff_lr[1]
    totalsum2=totalsum2+numbers[0]-diff_lr[0]   

print("Part 1", totalsum1)
print("Part 2", totalsum2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
