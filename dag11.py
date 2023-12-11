# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 05:58:36 2023

@author: Paul
"""
import itertools as it

import time
start_time = time.time_ns()

def galaxy_dist(galaxy1,galaxy2):
    return abs(galaxy1[1]-galaxy2[1])+abs(galaxy1[2]-galaxy2[2])

f = open("input_dag11.txt", "r")

time_factor=1000000-1
galaxy=0
galaxy_list=list()

galaxy_map=list()
for i,line in enumerate(f):
    line=line.replace('(','').replace(')','').replace('=','').replace('\n','').replace(',','')
    galaxy_map.append(line)
f.close()    

#horizontal expansion
hor_expansion=list()
for j,c in enumerate(galaxy_map[0]):
    hor_line=''
    for i in range(len(galaxy_map)):
        hor_line=hor_line+galaxy_map[i][j]
    if set(hor_line)=={'.'}:   
        hor_expansion.append(j)
    

#get galaxies using vertical expansion on the fly  
y_expansion=0  
for i,line in enumerate(galaxy_map):
    if set(line) == {'.'}:
        y_expansion=y_expansion+time_factor #keep track of y expansion
        continue

    for j,c in enumerate(line):
        if c=='#':  
            #find x expansion by comparing with horexp_list
            x_expansion=0
            for hor in hor_expansion:
                if j>hor:
                    x_expansion=x_expansion+time_factor
            
            galaxy_list.append([galaxy,j+x_expansion,i+y_expansion])
            galaxy=galaxy+1



#list of galaxis in galaxy_list galaxy,x,y
small_dist=999999
iters=0
total_distance=0

for a in it.combinations(galaxy_list,2):
    galaxy1=a[0]
    galaxy2=a[1]    
    iters=iters+1
    distance = galaxy_dist(galaxy1,galaxy2)
    print(galaxy1,galaxy2,distance)
    total_distance=total_distance+distance
    
    if distance < small_dist:
        small_dist=distance
    
print(total_distance)
print("--- %s ms ---" % ((time.time_ns() - start_time)/1000000))