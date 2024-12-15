# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 05:56:49 2023

@author: Paul
"""
import time
#import numpy as np
start_time = time.time_ns()



def hash_function(string):
    value=0
    for c in string:
        #value=value+ord(c)
        #value=value*17
        #value=value%256
        value=((value+ord(c))*17)%256
        
    return value




f = open("input_dag15.txt", "r")
for i,line in enumerate(f):
    strings=line.replace('\n','').split(',')
    #groups = list(map(int,line.split(',')))
f.close()
score1=0
for string in strings:
    score1+=hash_function(string)


lens_focal={}

boxes = [[] for i in range(256)]
for instr in strings:
    
    if '=' in instr:
        label=instr.split('=')[0]
        focal_length=int(instr.split('=')[1])
        
        box_n = hash_function(label)
        
        if boxes[box_n] != None:
            if (label in boxes[box_n])==False:           
                boxes[box_n].append(label)
        else:
            boxes[box_n].append(label)
            
        lens_focal.update({label:focal_length})
        
    if '-' in instr:
        label=instr.split('-')[0]
        box_n = hash_function(label)
        if boxes[box_n] != None:
            if label in boxes[box_n]:
                boxes[box_n].remove(label)

score2=0
for n,box in enumerate(boxes):
    if box != None:
        box_size=len(box)
        for i,lens in enumerate(box):
            score2+=(n+1)*(i+1)*lens_focal[lens]

print(score1)
print(score2)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
