# -*- coding: utf-8 -*-
"""
Created on Mon Dec 18 05:34:16 2023

@author: Paul
"""
import time
import numpy as np
start_time = time.time_ns()
import matplotlib.pyplot as plt


def poly_area(vertices): #Trapezoid formula
    area = 0
    if vertices[0] != vertices[-1]:
        vertices.append(vertices[0]) #sluit de loop als dat nog niet zo is
    
    for i,vertex in enumerate(vertices[:-1]):
        area += (vertex[1]+vertices[i+1][1])*(vertex[0]-vertices[i+1][0])
    return abs(0.5*area)

def vertices(instr):
    # key UL, UR etc   [offset_x, offset_y]
    offsets={'01':[ 0.5, 0.5],
             '03':[-0.5, 0.5],
             '10':[ 0.5, 0.5],
             '12':[ 0.5,-0.5],
             '21':[ 0.5,-0.5],
             '23':[-0.5,-0.5],
             '30':[-0.5, 0.5],
             '32':[-0.5,-0.5]}
    #directions key: xy
    directions={'0':[1,0],'1':[0,-1],'2':[-1,0],'3':[0,1]}
                             
    #Add one to the list to fix the beginning         
    instr.append(instr[0])
    
    #Left handed and right handed list
    vert_L = list()
    vert_R = list() 
    
    prev_direction=instr[0][0]
    loc_x=instr[0][1]*directions[instr[0][0]][0] #length * direction
    loc_y=instr[0][1]*directions[instr[0][0]][1]
    
    for [direction,length] in instr[1:]:
        offset_key=prev_direction+direction
        vert_L.append([loc_x+offsets[offset_key][0],loc_y+offsets[offset_key][1]])
        vert_R.append([loc_x-offsets[offset_key][0],loc_y-offsets[offset_key][1]])
        prev_direction=direction
        
        loc_x+=length*directions[direction][0]
        loc_y+=length*directions[direction][1]
    return vert_L,vert_R


directions={'U':'3','D':'1','L':'2','R':'0'}
f = open("input_dag18.txt", "r")

instr_p1=list()
instr_p2=list()

for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','')
    [direction,length,color] =line.split(' ')
    instr_p1.append([directions[direction],int(length)])
    instr_p2.append([color[-1],int(color[1:-1],16)])
f.close()

loop_L1,loop_R1 = vertices(instr_p1)
area1L = poly_area(loop_L1)
area1R = poly_area(loop_R1)


loop_L2,loop_R2 = vertices(instr_p2)
area2L = poly_area(loop_L2)
area2R = poly_area(loop_R2)

  
print("Part 1",int(max(area1L,area1R)))
print("Part 2",int(max(area2L,area2R)))
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))
